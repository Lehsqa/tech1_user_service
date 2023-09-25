import random

from faker import Faker

from fastapi_limiter import FastAPILimiter

from project.app.application.users import create
from project.app.domain.articles import ArticleRepository, ArticleUncommited
from project.app.domain.users import User
from project.app.infrastructure.database import Base
from project.app.infrastructure.database.session import engine


fake = Faker()


async def create_random_users_articles(num_users: int = random.randint(5, 10)):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    for _ in range(num_users):
        user: User = await create(payload={
            "name": fake.name(),
            "age": random.randint(18, 60),
            "password": "qwerty"
        })
        for _ in range(random.randint(1, 5)):
            await ArticleRepository().create(
                ArticleUncommited(
                    text="Test",
                    color=random.choice(["red", "green", "blue"]),
                    author_id=user.id
                )
            )


async def rate_limiter():
    import redis.asyncio as redis
    redis = redis.from_url("redis://redis", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
