
from chat.models.chat_model import Message
import fastapi
import chat.controller.chat_controller as chatController 

router = fastapi.APIRouter()

@router.post("/send-message")
async def send_text(
    convo: str = fastapi.Form(...), 
    file: fastapi.UploadFile = fastapi.File(None)
):
    message = Message(convo=convo)
    res = await chatController.sendText(message)
    print(res)
    return res