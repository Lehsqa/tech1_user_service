from typing import AsyncGenerator

from project.app.infrastructure.database import BaseRepository, UsersTable, ArticleTable

from .models import User, UserUncommited, UserNamePublic


class UsersRepository(BaseRepository[UsersTable]):
    schema_class = UsersTable
    schema_class_join = ArticleTable

    async def get(self, id_: int) -> User:
        instance = await self._get(key="id", value=id_)
        return User.model_validate(instance)

    async def get_all(self, color_: str) -> AsyncGenerator[User, None]:
        async for instance in self._get_all(relationship="articles", key="color", value=color_):
            yield User.model_validate(instance)

    async def get_all_filter(self) -> AsyncGenerator[UserNamePublic, None]:
        async for instance in self._get_all_filter(column="name", relationship="articles", value=3):
            yield UserNamePublic.model_validate({'name': instance})

    async def filter(self, age_: int) -> AsyncGenerator[User, None]:
        async for instance in self._filter(key="age", value=age_):
            yield User.model_validate(instance)

    async def create(self, schema: UserUncommited) -> User:
        instance: UsersTable = await self._save(schema.model_dump())
        return User.model_validate(instance)
