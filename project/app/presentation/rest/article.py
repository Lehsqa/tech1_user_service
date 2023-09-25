import os

from fastapi import APIRouter, Depends, Request, status

from fastapi_limiter.depends import RateLimiter

from project.app.application.authentication import JWTBearer
from project.app.domain.articles import (
    Article,
    ArticleCreateRequestBody,
    ArticlePublic,
    ArticleRepository,
    ArticleUncommited
)

router = APIRouter(prefix="/article", tags=["Article"])
times: int = int(os.environ.get("LIMITER_TIMES"))
seconds: int = int(os.environ.get("LIMITER_SECONDS"))


@router.post("", dependencies=[Depends(JWTBearer()), Depends(RateLimiter(times=times, seconds=seconds))],
             status_code=status.HTTP_201_CREATED)
async def article_create(
    _: Request,
    schema: ArticleCreateRequestBody,
) -> ArticlePublic:
    article: Article = await ArticleRepository().create(
        ArticleUncommited(**schema.model_dump())
    )

    return ArticlePublic.model_validate(article)
