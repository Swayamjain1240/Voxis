from fastapi import APIRouter

from app.schemas.sign import SignInferenceRequest
from app.services.sign_recognition.inference import (
    SignInferenceService,
)


router = APIRouter()

sign_service = SignInferenceService()


@router.get("/status")
async def status():
    return sign_service.status()


@router.post("/predict")
async def predict(
    payload: SignInferenceRequest,
):
    return await sign_service.predict(
        payload.model_dump()
    )
