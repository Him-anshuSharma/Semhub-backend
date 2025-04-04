
from chat.models.chat_model import Message
from init import gemini
import constants
import asyncio

async def sendText(message: Message, timetable: str):
    response = await asyncio.to_thread(
        gemini.models.generate_content,
        model="gemini-2.0-flash",
        contents=[constants.CHAT_PROMPT + ". Here is the Timetable: " + timetable, message.convo]
    )
    return response.text