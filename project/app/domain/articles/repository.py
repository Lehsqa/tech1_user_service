from typing import AsyncGenerator

from project.app.infrastructure.database import BaseRepository, ArticleTable

from .models import Article, ArticleUncommited


class ArticleRepository(BaseRepository[ArticleTable]):
    schema_class = ArticleTable

    async def create(self, schema: ArticleUncommited) -> Article:
        instance: ArticleTable = await self._save(schema.model_dump())
        return Article.model_validate(instance)
