"""Deny-by-default dependencies for future private routes; no login is simulated."""
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request


@dataclass(frozen=True)
class Principal:
    subject: str
    permissions: frozenset[str]


def require_principal(request: Request) -> Principal:
    principal = getattr(request.state, "principal", None)
    if not isinstance(principal, Principal):
        # Only a future trusted authentication verifier may set this state.
        # Headers, cookies and request JSON are never treated as identity here.
        raise HTTPException(401, "Authentication is required.")
    return principal


def require_permission(permission: str):
    def check(principal: Principal = Depends(require_principal)):
        if permission not in principal.permissions:
            raise HTTPException(403, "Permission denied.")
        return principal
    return check


def require_owner(principal: Principal, owner_id: str):
    if principal.subject != owner_id:
        raise HTTPException(403, "Resource access denied.")
