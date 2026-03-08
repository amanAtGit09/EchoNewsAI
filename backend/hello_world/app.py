import json
from decimal import Decimal
import uuid
import time
from news_service import fetch_news
from ai_service import generate_summary
from audio_service import generate_voice
from storage_service import save_to_cloud, get_news_from_db, get_latest_news_by_category

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    
    if event.get('source') == 'aws.events':
        import datetime
        # AWS Lambda runs in UTC. Convert to IST (UTC + 5:30)
        ist_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=5, minutes=30)
        hour = ist_time.hour
        
        # Determine the label for the briefing
        if 5 <= hour < 11:
            time_label = "Morning"
        elif 11 <= hour < 17:
            time_label = "Afternoon"
        else:
            time_label = "Evening"
            
        return run_full_pipeline(category="breaking", news_type="BRIEFING", time_label=time_label)

    # API extraction logic
    req_type = query_params.get('type', 'briefing')
    category = query_params.get('category', None)
    
    try:
        if req_type == 'pipeline':
            search_query = query_params.get('q')
            search_category = query_params.get('category', 'top') # Default to 'top'
            return run_full_pipeline(search_category, search_query, news_type="CUSTOM")
        elif req_type == 'history':
            data = get_latest_news_by_category(category, is_briefing=False, limit=10)
            return respond(200, data)
        else:
            data = get_latest_news_by_category(category="breaking", is_briefing=True, limit=3)
            return respond(200, data)
    except Exception as e:
        return respond(500, {"error": str(e)})

def run_full_pipeline(category, query=None, country='in', lang='en', news_type="CUSTOM", time_label=None):
    # If it's a briefing, include the time_label in the ID for easy UI identification
    label_suffix = f"#{time_label.upper()}" if time_label else ""
    briefing_id = f"{news_type}#{category.upper()}{label_suffix}#{int(time.time())}"
    
    articles = fetch_news(category=category, query=query, country=country, language=lang)
    if not articles:
        return respond(404, {"message": "No news found for these params"})
        
    # Pass time_label to AI for the custom intro
    script = generate_summary(articles, time_label=time_label)
    
    # Use 'Matthew' for professional briefings, 'Kajal' for custom news
    voice_id = 'Matthew' if time_label else 'Kajal'
    audio_stream = generate_voice(script, VoiceId=voice_id)
    
    if audio_stream is None:
        return respond(500, {"error": "Voice generation failed."})
    
    s3_key = save_to_cloud(briefing_id, category, news_type, articles, audio_stream)
    full_data = get_news_from_db(briefing_id)
    return respond(200, full_data)

# Add this helper class to handle DynamoDB Decimals
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert decimal to float or int
            return float(obj) if obj % 1 > 0 else int(obj)
        return super(DecimalEncoder, self).default(obj)

def respond(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        # Use the DecimalEncoder here!
        'body': json.dumps(body, cls=DecimalEncoder)
    }