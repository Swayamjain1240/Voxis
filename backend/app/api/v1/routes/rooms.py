from fastapi import APIRouter, HTTPException, Request, status
from app.schemas.response import success

from app.services.rooms.room_manager import room_manager


router = APIRouter()


@router.get("/status")
async def room_status(request: Request):
    return success(request, room_manager.status())


@router.post("")
async def create_room(request: Request):
    if not room_manager.enabled:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=(
                "Remote rooms are intentionally deferred. "
                "Mode 1 is the current MVP."
            ),
        )

    return success(request, room_manager.create_room())


@router.post("/join")
async def join_room(request: Request):
    if not room_manager.enabled:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=(
                "Remote rooms are intentionally deferred. "
                "Mode 1 is the current MVP."
            ),
        )

    return success(request, room_manager.join_room())
