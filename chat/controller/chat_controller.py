
from chat.models.chat_model import Message
from init import gemini
import constants
import asyncio

async def sendText(message: Message):

    response = await asyncio.to_thread(
        gemini.models.generate_content,
        model="gemini-2.0-flash",
        contents=[constants.CHAT_PROMPT, message.convo]
    )
    return response.text