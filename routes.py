from fastapi import APIRouter, Depends
from models.motivational_message import MotivationalMessageRequest
from services.create_motivational_message_service import CreateMotivationalMessageService
from services.auth_service import get_firebase_user

router = APIRouter()

@router.post("/create")
async def create_message(
    message: MotivationalMessageRequest,
    user: dict = Depends(get_firebase_user)
):
    service = CreateMotivationalMessageService()
    result = await service.execute(
        name=message.name,
        how_you_feel_currently=message.how_you_feel_currently,
        main_challenges=message.main_challenges,
        goals_dreams=message.goals_dreams,
        how_you_handle_emotions=message.how_you_handle_emotions,
        support_sources=message.support_sources,
        personal_care=message.personal_care
    )
    return {"data": result}
