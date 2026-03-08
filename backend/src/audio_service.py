import boto3

# Initialize Polly with the region you've been using
polly = boto3.client('polly', region_name='us-east-1')

def generate_voice(text, VoiceId='Kajal'):
    """
    Converts the EchoNews script into a high-quality MP3 stream.
    """
    try:
        # Check text length before calling Polly
        if len(text) > 3000:
            print(f"Text too long for Polly: {len(text)} chars")
            return None

        # We use Engine='neural' for the most human-like intonation
        response = polly.synthesize_speech(
            Engine='neural',
            Text=text,
            OutputFormat='mp3',
            VoiceId=VoiceId
        )
        
        return response['AudioStream'].read()
        
    except Exception as e:
        print(f"Polly error: {e}")
        return None

# Quick test if run directly
if __name__ == "__main__":
    test_text = """And finally, let’s get our adrenaline pumping! The national team has done it! They’ve clinched the championship after a truly dramatic final. The cheers, the nail-biting tension, the sheer elation – it’s what makes sports so captivating, isn't it? A reminder that with enough heart and hustle, victory is always within reach. 
    That’s all the buzz from EchoNews today.
    I'm Echo, and that's the word on the street.
    """
    audio = generate_voice(test_text)
    if audio:
        with open("echo_matthew.mp3", "wb") as f:
            f.write(audio)
        print("Success! Created 'echo_matthew.mp3'. Go ahead and listen to Matthew!")