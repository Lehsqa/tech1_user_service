from project.app.application.authentication.authentication import get_password_hash
from project.app.domain.users import (
    User,
    UsersRepository,
    UserUncommited
)


async def create(payload: dict) -> User:
    payload.update(password=get_password_hash(payload["password"]))

    user: User = await UsersRepository().create(
        UserUncommited(**payload)
    )
    return user
