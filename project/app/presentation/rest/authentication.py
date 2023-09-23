import os
from datetime import timedelta

from fastapi import APIRouter, Request, status, HTTPException

from project.app.application.authentication import authenticate_user, create_access_token
from project.app.domain.authentication import (
    TokenClaimPublic,
    TokenClaimRequestBody,
)

router = APIRouter(prefix="/token", tags=["Token"])


@router.post("", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    _: Request,
    schema: TokenClaimRequestBody,
) -> TokenClaimPublic:
    access_token_expires = timedelta(minutes=float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    token_payload = authenticate_user(schema, expires_delta=access_token_expires)
    if not token_payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(token_payload=token_payload)

    return TokenClaimPublic(access=access_token.raw_token)
