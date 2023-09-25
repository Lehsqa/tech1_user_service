import os

from fastapi import APIRouter, Depends, Request, status

from fastapi_limiter.depends import RateLimiter

from project.app.application.authentication import JWTBearer
from project.app.application.users import create
from project.app.domain.users import (
    User,
    UserCreateRequestBody,
    UserPublic,
    UsersRepository,
    UserNamePublic
)

router = APIRouter(prefix="/users", tags=["Users"])
times: int = int(os.environ.get("LIMITER_TIMES"))
seconds: int = int(os.environ.get("LIMITER_SECONDS"))


@router.get("", dependencies=[Depends(JWTBearer()), Depends(RateLimiter(times=times, seconds=seconds))],
            status_code=status.HTTP_200_OK)
async def users_list(id: int, request: Request) -> UserPublic:
    user_public: User = await UsersRepository().get(id_=id)

    return UserPublic.model_validate(user_public)


@router.post("", dependencies=[Depends(JWTBearer()), Depends(RateLimiter(times=times, seconds=seconds))],
             status_code=status.HTTP_201_CREATED)
async def user_create(
    _: Request,
    schema: UserCreateRequestBody,
) -> UserPublic:
    user: User = await create(payload=schema.model_dump())

    return UserPublic.model_validate(user)


@router.get("/age", dependencies=[Depends(JWTBearer()), Depends(RateLimiter(times=times, seconds=seconds))],
            status_code=status.HTTP_200_OK)
async def filter_age(age: int, request: Request) -> list[UserPublic]:
    users_filter = [
        UserPublic.model_validate(user)
        async for user in UsersRepository().filter(age_=age)
    ]

    return users_filter


@router.get("/users_by_color", dependencies=[Depends(JWTBearer()), Depends(RateLimiter(times=times, seconds=seconds))],
            status_code=status.HTTP_200_OK)
async def filter_users_by_color(color: str, request: Request) -> list[UserPublic]:
    users_filter = [
        UserPublic.model_validate(user)
        async for user in UsersRepository().get_all(color_=color)
    ]

    return users_filter


@router.get("/unique_names", dependencies=[Depends(JWTBearer()), Depends(RateLimiter(times=times, seconds=seconds))],
            status_code=status.HTTP_200_OK)
async def filter_unique_names(request: Request) -> list[UserNamePublic]:
    users_filter = [
        UserNamePublic.model_validate(user)
        async for user in UsersRepository().get_all_filter()
    ]

    return users_filter
