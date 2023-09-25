from fastapi import FastAPI

from project.app.startup_tasks import create_random_users_articles, rate_limiter
from project.app.presentation import rest
from project.app.infrastructure import application


app: FastAPI = application.create(
    rest_routers=(rest.users.router, rest.authentication.router, rest.article.router),
    startup_tasks=[create_random_users_articles, rate_limiter],
    shutdown_tasks=[]
)
