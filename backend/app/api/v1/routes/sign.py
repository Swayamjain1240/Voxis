from fastapi import APIRouter, Request

from app.schemas.sign import SignInferenceRequest
from app.services.sign_recognition.inference import (
    SignInferenceService,
)
from app.schemas.response import ApiResponse, success
from app.schemas.sign import SignPredictionResult


router = APIRouter()

sign_service = SignInferenceService()


@router.get("/status")
async def status(request: Request):
    return success(request, sign_service.status())


@router.post("/predict", response_model=ApiResponse[SignPredictionResult])
async def predict(
    request: Request,
    payload: SignInferenceRequest,
):
    result = await sign_service.predict(
        payload.model_dump()
    )
    return success(request, result)
