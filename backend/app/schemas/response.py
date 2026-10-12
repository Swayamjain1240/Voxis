from typing import Generic, Literal, TypeVar
from uuid import uuid4

from fastapi import Request

from app.schemas.common import ContractModel, Version


T = TypeVar("T")


class ResponseMeta(ContractModel):
    request_id: str
    api_version: Literal["v1"] = "v1"
    schema_version: Version = "1.0.0"


class ApiResponse(ContractModel, Generic[T]):
    success: Literal[True] = True
    data: T
    meta: ResponseMeta


def request_meta(request: Request | None) -> dict:
    state = request.scope.setdefault("state", {}) if request is not None else {}
    request_id = state.setdefault("request_id", uuid4().hex)
    return ResponseMeta(request_id=request_id).model_dump()


def success(request: Request, data):
    return {"success": True, "data": data, "meta": request_meta(request)}
