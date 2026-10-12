from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.api.v1.router import api_router
from app.core.config import Settings, settings
from app.core.exceptions import http_exception_handler, unhandled_exception_handler, validation_exception_handler
from app.core.logging import configure_logging
from app.core.request_context import RequestContextMiddleware
from app.core.transport import TransportMiddleware
from app.schemas.response import success


@asynccontextmanager
async def lifespan(_app):
    logger = configure_logging()
    logger.info("VOXIS backend starting | phase=1 | mode=mode-1")
    yield
    logger.info("VOXIS backend shutting down")


def create_app(config: Settings = settings):
    app = FastAPI(
        title=config.app_name, version="0.1.0", debug=config.debug,
        description="VOXIS restricted-vocabulary communication foundation.",
        docs_url=None, redoc_url=None,
        openapi_url="/openapi.json" if config.environment in {"development", "test"} else None,
        lifespan=lifespan,
    )
    app.state.settings = config
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_middleware(TransportMiddleware, settings=config)
    app.add_middleware(RequestContextMiddleware)
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", tags=["system"])
    async def root(request: Request):
        return success(request, {
            "name": config.app_name, "status": "running", "phase": 1,
            "mode": "mode-1", "docs": app.openapi_url,
        })

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        # Mode 1 uses REST. Re-enabling sockets requires a separately reviewed
        # authenticated/isolated protocol; configuration cannot enable this route.
        await websocket.close(code=1008, reason="WebSocket transport is disabled.")

    return app


app = create_app()
