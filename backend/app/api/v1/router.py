from fastapi import APIRouter

from app.api.v1.routes.conversation import router as conversation_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.rooms import router as rooms_router
from app.api.v1.routes.sign import router as sign_router
from app.api.v1.routes.speech import router as speech_router


api_router = APIRouter()

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["health"],
)

api_router.include_router(
    speech_router,
    prefix="/speech",
    tags=["speech"],
)

api_router.include_router(
    sign_router,
    prefix="/sign",
    tags=["sign"],
)

api_router.include_router(
    conversation_router,
    prefix="/conversation",
    tags=["conversation"],
)

api_router.include_router(
    rooms_router,
    prefix="/rooms",
    tags=["rooms"],
)
