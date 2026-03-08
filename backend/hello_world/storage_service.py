import boto3
import time
import datetime
from botocore.exceptions import ClientError
from botocore.config import Config

# This config forces AWS to use the modern "v4" signature
s3 = boto3.client(
    's3', 
    region_name='us-east-1',
    # This config is the secret sauce for private bucket access
    config=Config(
        signature_version='s3v4',
        s3={'addressing_style': 'virtual'} 
    )
)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('EchoNewsTable')

BUCKET_NAME = "echonews-audio-2026"

def save_to_cloud(briefing_id, category, news_type, headlines, audio_stream):
    """
    Saves audio to S3 and metadata to DynamoDB with smart TTL and sortable ISO dates.
    """
    s3_key = f"audio/{briefing_id}.mp3"
    
    # 1. Upload Audio to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=audio_stream,
        ContentType="audio/mpeg"
    )

    # 2. Determine TTL (24h for Briefings, 7 days for Custom/Category)
    days = 1 if news_type == "BRIEFING" else 7
    ttl_timestamp = int(time.time()) + (days * 86400)

    # 3. Save to DynamoDB
    # FIX: Use ISO format so "latest" queries actually find the newest items
    now_iso = datetime.datetime.now().isoformat()

    table.put_item(
        Item={
            'BriefingID': briefing_id,
            'Type': news_type,
            'Category': category,
            'Headlines': headlines,
            'S3AudioKey': s3_key,
            'TimeToLive': ttl_timestamp,
            'CreatedAt': now_iso # Permanent fix for sorting
        }
    )
    return s3_key


def get_news_from_db(briefing_id):
    """
    Fetches news and generates a FRESH 2-hour pre-signed URL.
    """
    try:
        response = table.get_item(Key={'BriefingID': briefing_id})
        if 'Item' not in response:
            return None
        
        item = response['Item']
        
        # Generate fresh URL for the stored key
        audio_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': item['S3AudioKey']},
            ExpiresIn=7200 # 2 hours
        )
        
        item['audio_url'] = audio_url
        return item
    except ClientError as e:
        print(f"DB Fetch Error: {e}")
        return None


from boto3.dynamodb.conditions import Key, Attr

def get_latest_news_by_category(category, is_briefing=False, limit=3):
    try:
        if is_briefing:
            # We use a higher internal limit (50) to find briefings among search results,
            # but still only return the 'limit' requested by the UI (3)
            response = table.query(
                IndexName='CategoryIndex',
                KeyConditionExpression=Key('Category').eq(category),
                FilterExpression=Attr('Type').eq('BRIEFING'),
                ScanIndexForward=False, 
                Limit=50 # Permanent fix for the "Limit vs Filter" trap
            )
        else:
            response = table.query(
                IndexName='CategoryIndex',
                KeyConditionExpression=Key('Category').eq(category),
                ScanIndexForward=False,
                Limit=limit
            )

        items = response.get('Items', [])
        
        # Ensure we only return the amount the UI actually asked for
        final_items = items[:limit]

        for item in final_items:
            item['audio_url'] = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET_NAME, 'Key': item['S3AudioKey']},
                ExpiresIn=7200
            )
            
        return final_items 
    except Exception as e:
        print(f"Error querying DB: {e}")
        return []
    
if __name__ == "__main__":
    # Mock data to test save_to_cloud
    test_id = "TEST-ID-003"
    test_headlines = [{"title": "Test News", "description": "This is a storage test."}]
    test_audio = b"fake-audio-content" # Mock binary
    
    print("Testing Storage Upload...")
    key = save_to_cloud(test_id, "technology", "CUSTOM", test_headlines, test_audio)
    print(f"Uploaded to S3: {key}")
    
    print("Testing DB Fetch...")
    data = get_news_from_db(test_id)
    if data:
        print(f"Success! Found DB record with URL: {data['audio_url']}")