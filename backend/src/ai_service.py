import os
import json
import boto3
from google import genai
from dotenv import load_dotenv

load_dotenv()

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1') # aws service client for Nova
api_key = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=api_key) # gemini client for fallback if Nova is unavailable

def generate_summary(articles, use_nova=True, time_label=None):
    """
    Creates a catchy radio briefing. 
    Fallbacks to Gemini if Nova is disabled or throttled.
    """
    context_text = "\n".join([f"TITLE: {a['title']}\nSUMMARY: {a['description']}\n---" for a in articles])

    # Dynamic intro based on time of day
    intro_segment = ""
    if time_label:
        intro_segment = f"Good {time_label}, India! This is your Echo {time_label} briefing. Let's look at the top stories making headlines right now."

    prompt = f"""
    You are 'Echo', a professional news anchor for EchoNews.
    {f"Intro: {intro_segment}" if time_label else "Tone: Professional, clear, and engaging."}
    
    TASK:
    Generate a continuous radio-style news script based strictly on these articles:
    {context_text}
    
    STRICT REPORTING GUIDELINES:
    - {f'Start exactly with: "{intro_segment}"' if time_label else 'Start with a brief, professional greeting.'}
    - FACTUAL FOCUS: Use the title and description to construct a complete, informative narrative for each story. 
    - NO OPINIONS: Do not add your own thoughts, jokes, or observations. Stay focused on the provided information.
    - ONLY output the spoken words. No music cues, no stage directions, no [bracketed] text.
    - SEAMLESS FLOW: Use short, professional transitions between stories (e.g., "Turning to the world of sports," or "In other news today...").
    - NO FILLER: Avoid phrases like "You might find this interesting" or "It's a crazy world." Just give the facts.
    - End exactly with: "I'm Echo, and that's the word on the street."
    - MAXIMUM LENGTH: 2400 characters.
    
    SPOKEN SCRIPT:
    """

    if use_nova:
        try:
            return _call_nova(prompt)
        except Exception as e:
            print(f"AWS Nova check failed ({e}). Defaulting to Gemini...")
            return _call_gemini(prompt)
    else:
        return _call_gemini(prompt)

def _call_nova(prompt):
    # Modern Messages API for Nova
    body = json.dumps({
        "inferenceConfig": {"maxTokens": 1000, "temperature": 0.8},
        "messages": [{"role": "user", "content": [{"text": prompt}]}]
    })
    
    response = bedrock.invoke_model(
        modelId="amazon.nova-micro-v1:0", 
        body=body
    )
    
    response_json = json.loads(response.get('body').read())
    return response_json['output']['message']['content'][0]['text'].strip()

def _call_gemini(prompt):
    # Using the new Client-based syntax for Gemini 2.5 Flash-Lite
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

# Test with mock data
if __name__ == "__main__":
    mock_articles = [
    {
        "title": "AI Ethics Debate",
        "description": "Global tech leaders gather in Geneva to discuss ethical frameworks for artificial intelligence, focusing on transparency and accountability."
    },
    {
        "title": "Mars Mission Milestone",
        "description": "NASA’s Perseverance rover successfully deploys a new drone to explore Martian terrain, marking a breakthrough in autonomous planetary research."
    },
    {
        "title": "Economic Outlook",
        "description": "International Monetary Fund releases a report predicting steady global growth, driven by renewable energy investments and digital transformation."
    },
    {
        "title": "Medical Innovation",
        "description": "Scientists unveil a revolutionary blood test capable of detecting multiple cancers at early stages, raising hopes for improved survival rates."
    },
    {
        "title": "Climate Action Pact",
        "description": "Over 50 nations sign a landmark agreement to phase out coal by 2035, signaling a major step toward reducing greenhouse gas emissions."
    },
    {
        "title": "Tech Acquisition",
        "description": "A leading cloud provider acquires a cybersecurity startup to strengthen defenses against rising ransomware attacks worldwide."
    },
    {
        "title": "Historic Sports Triumph",
        "description": "Underdog team clinches victory in the continental football championship, sparking nationwide celebrations and calls for increased youth training programs."
    }
]

    # Run with use_nova=False to test your Gemini connection first
    print(generate_summary(mock_articles, use_nova=False, time_label="Evening"))