from typing import Any, AsyncGenerator, Generic, Type

from sqlalchemy import Result, func, select

from project.app.infrastructure.database.session import Session
from project.app.infrastructure.database.tables import ConcreteTable
from project.app.infrastructure.errors import (
    DatabaseError,
    NotFoundError,
    UnprocessableError,
)


class BaseRepository(Session, Generic[ConcreteTable]):  # type: ignore
    """This class implements the base interface for working with database
    # and makes it easier to work with type annotations.
    """

    schema_class: Type[ConcreteTable]
    schema_class_join = Type[ConcreteTable]

    def __init__(self) -> None:
        super().__init__()

        if not self.schema_class:
            raise UnprocessableError(
                message=(
                    "Can not initiate the class without schema_class attribute"
                )
            )

    async def _filter(self, key: str, value: int) -> AsyncGenerator[ConcreteTable, None]:
        query = select(
            self.schema_class
        ).where(
            getattr(self.schema_class, key) > value
        )
        result: Result = await self.execute(query)
        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def _get(self, key: str, value: Any) -> ConcreteTable:
        query = select(
            self.schema_class
        ).where(
            getattr(self.schema_class, key) == value
        )
        result: Result = await self.execute(query)

        if not (_result := result.scalars().one_or_none()):
            raise NotFoundError

        return _result

    async def _get_all(self, relationship: str, key: str, value: Any) -> AsyncGenerator[ConcreteTable, None]:
        query = select(
            self.schema_class
        ).join(
            getattr(self.schema_class, relationship)
        ).where(
            getattr(self.schema_class_join, key) == value
        ).distinct()
        result: Result = await self.execute(query)
        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def _get_all_filter(self, column: str, relationship: str, value: int) -> AsyncGenerator[ConcreteTable, None]:
        query = select(
            getattr(self.schema_class, column)
        ).join(
            getattr(self.schema_class, relationship)
        ).group_by(
            getattr(self.schema_class, column)
        ).having(
            func.count(getattr(self.schema_class_join, "id")) > value
        )
        result: Result = await self.execute(query)
        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def _save(self, payload: dict[str, Any]) -> ConcreteTable:
        schema = self.schema_class(**payload)
        await self.save(schema)
        return schema
