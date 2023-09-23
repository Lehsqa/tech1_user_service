from pydantic import Field

from project.app.infrastructure.models import InternalModel, PublicModel


# Public models
# ------------------------------------------------------
class _UserName(PublicModel):
    name: str = Field(description="OpenAPI desc")


class _UserPublic(_UserName):
    age: int = Field(description="OpenAPI desc")


class UserCreateRequestBody(_UserPublic):
    password: str


class UserNamePublic(_UserName):
    pass


class UserPublic(_UserPublic):
    id: int


# Internal models
# ------------------------------------------------------
class UserUncommited(InternalModel):
    name: str
    password: str
    age: int


class User(UserUncommited):
    id: int
