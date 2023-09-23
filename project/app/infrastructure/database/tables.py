from enum import Enum
from typing import TypeVar

from sqlalchemy import Column, Integer, String, Enum as EnumType, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class _Base:
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=_Base, metadata=meta)

ConcreteTable = TypeVar("ConcreteTable", bound=Base)


class ColorEnum(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class UsersTable(Base):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    articles = relationship("ArticleTable", back_populates="author")


class ArticleTable(Base):
    __tablename__ = "articles"

    text = Column(String, nullable=False)
    color = Column(EnumType(ColorEnum), nullable=False)
    author_id = Column(ForeignKey(UsersTable.id))
    author = relationship("UsersTable", back_populates="articles")
