from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.cors import configure_cors
from app.core.logging import configure_logging
from app.websocket.events import build_event
from app.websocket.manager import connection_manager


configure_logging()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger = configure_logging()
    logger.info(
        "VOXIS backend starting | environment=%s | phase=1",
        settings.environment,
    )

    yield

    logger.info("VOXIS backend shutting down")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Backend for VOXIS / SilentSign ? "
        "two-way Indian Sign Language communication."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

configure_cors(app)

app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/", tags=["system"])
async def root():
    return {
        "name": settings.app_name,
        "status": "running",
        "environment": settings.environment,
        "phase": 1,
        "mode": "mode-1",
        "docs": "/docs",
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)

    try:
        await websocket.send_json(
            build_event(
                "system.ready",
                {
                    "message": "VOXIS WebSocket connected",
                    "mode": "mode-1",
                },
            )
        )

        while True:
            payload = await websocket.receive_json()

            event_type = payload.get(
                "type",
                "conversation.message",
            )

            event_data = payload.get(
                "data",
                payload,
            )

            await connection_manager.broadcast(
                build_event(
                    event_type,
                    event_data,
                )
            )

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

    except Exception:
        connection_manager.disconnect(websocket)
        raise
