from fastapi import APIRouter
from yt_transcript.controllers.yt_transcript_controller import get_transcript

router = APIRouter()

@router.post("/get_transcripts")
def get_transcripts(urls: list[str]):
    transcripts = []
    for url in urls:
        transcript = get_transcript(url)
        transcripts.append(transcript)
    return transcripts