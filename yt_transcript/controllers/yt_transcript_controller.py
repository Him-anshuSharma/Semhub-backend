from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()

def get_transcript(video_id):
    try:
        transcript = ytt_api.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return []
    
def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return None

def get_transcript_from_urls(urls):
    transcripts = []
    for url in urls:
        video_id = get_video_id(url)
        if video_id:
            transcript = get_transcript(video_id)
            if transcript:
                transcripts.append(transcript)
    return transcripts

def format_transcripts(transcripts):
    formatted_transcripts = []
    for transcript in transcripts:
        formatted_transcript = ""
        for line in transcript:
            formatted_transcript += line['text'] + " "
        formatted_transcripts.append(formatted_transcript)
    return formatted_transcripts

