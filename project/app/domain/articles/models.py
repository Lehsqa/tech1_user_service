from pydantic import Field

from project.app.infrastructure.models import InternalModel, PublicModel


# Public models
# ------------------------------------------------------
class _ArticlePublic(PublicModel):
    text: str = Field(description="OpenAPI desc")
    color: str = Field(description="OpenAPI desc")


class ArticleCreateRequestBody(_ArticlePublic):
    author_id: int


class ArticlePublic(_ArticlePublic):
    id: int


# Internal models
# ------------------------------------------------------
class ArticleUncommited(InternalModel):
    text: str
    color: str
    author_id: int


class Article(ArticleUncommited):
    id: int
