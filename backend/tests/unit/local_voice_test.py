import boto3

polly = boto3.client('polly', region_name='us-east-1')

def make_audio():
    print("Synthesizing voice...")
    try:
        response = polly.synthesize_speech(
            Text="Testing one two three. Aman, your news system is almost ready!",
            OutputFormat='mp3',
            VoiceId='Joanna'
        )
        
        if "AudioStream" in response:
            with open("greeting.mp3", "wb") as f:
                f.write(response['AudioStream'].read())
            print("Done! Open 'greeting.mp3' in your folder to hear it.")
    except Exception as e:
        print(f"Polly error: {e}")

if __name__ == "__main__":
    make_audio()