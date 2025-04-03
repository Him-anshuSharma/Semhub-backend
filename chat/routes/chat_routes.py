
from chat.models.chat_model import Message
import fastapi
import chat.controller.chat_controller as chatController 

router = fastapi.APIRouter()

@router.post("/send-message")
async def sendText(message: Message):
    res = await chatController.sendText(message)
    print(res)
    return res