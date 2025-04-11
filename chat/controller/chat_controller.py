
from chat.models.chat_model import Message
from init import gemini
import constants
import asyncio

import json

def clean_json_string(raw_input: str):
    try:
        # Remove escape characters if present (common in stringified JSON)
        if "\\\"" in raw_input or "\\n" in raw_input:
            raw_input = raw_input.encode().decode('unicode_escape')

        # Try to parse it
        data = json.loads(raw_input)

        # Confirm it's a dictionary or list
        if isinstance(data, (dict, list)):
            return data
        else:
            raise ValueError("Parsed content is not a valid JSON object or array.")

    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)
    except Exception as e:
        print("Error:", e)

    return None


async def sendText(message: Message, timetable: str):
    response = await asyncio.to_thread(
        gemini.models.generate_content,
        model="gemini-2.0-flash",
        contents=[constants.CHAT_PROMPT, "Here is the Timetable: " + timetable, "chat history: "+message.convo]
    )
    return clean_json_string(response.text.replace('```','').replace('json',''))