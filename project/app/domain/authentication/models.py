from pydantic import Field

from project.app.infrastructure.models import InternalModel, PublicModel


# Public models
# ------------------------------------------------------
class TokenClaimRequestBody(PublicModel):
    login: str = Field(description="OpenAPI documentation")
    password: str = Field(description="OpenAPI documentation")


class TokenClaimPublic(PublicModel):
    access: str = Field(description="OpenAPI documentation")


# Internal models
# ------------------------------------------------------
class TokenPayload(InternalModel):
    sub: str
    exp: float


class AccessToken(InternalModel):
    payload: TokenPayload
    raw_token: str


class RefreshToken(InternalModel):
    payload: TokenPayload
    raw_token: str
