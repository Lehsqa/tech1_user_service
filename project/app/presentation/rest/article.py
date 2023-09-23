from fastapi import APIRouter, Depends, Request, status

from project.app.application.authentication import JWTBearer
from project.app.domain.articles import (
    Article,
    ArticleCreateRequestBody,
    ArticlePublic,
    ArticleRepository,
    ArticleUncommited
)

router = APIRouter(prefix="/article", tags=["Article"])


@router.post("", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def article_create(
    _: Request,
    schema: ArticleCreateRequestBody,
) -> ArticlePublic:
    article: Article = await ArticleRepository().create(
        ArticleUncommited(**schema.model_dump())
    )

    return ArticlePublic.model_validate(article)
