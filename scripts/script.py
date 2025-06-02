from fastapi import APIRouter, HTTPException
from models.motivational_message import MotivationalMessageRequest, MotivationalMessageResponse
from services.create_motivational_message_service import CreateMotivationalMessageService

router = APIRouter()

@router.get("/teste")
async def test_endpoint():
    response_data = {
        "nome": "Ana",
        "mensagem": "Ei, Ana! Deus está contigo em cada passo! 'Tudo posso naquele que me fortalece' (Filipenses 4:13). Continue brilhando!"
    }
    return {"data": response_data}

@router.post("/create", response_model=MotivationalMessageResponse)
async def create_motivational_message(request: MotivationalMessageRequest):
    try:
        service = CreateMotivationalMessageService()
        result = await service.execute(
            name=request.name,
            how_you_feel_currently=request.how_you_feel_currently,
            main_challenges=request.main_challenges,
            goals_dreams=request.goals_dreams,
            how_you_handle_emotions=request.how_you_handle_emotions,
            support_sources=request.support_sources,
            personal_care=request.personal_care
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))