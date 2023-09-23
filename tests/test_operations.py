from httpx import AsyncClient

from project.app.application.users import create
from project.app.domain.users import User, UsersRepository


async def test_create_token(ac: AsyncClient):
    response = await ac.post("/token", json={
        "login": "string",
        "password": "string"
    })

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, dict)


async def test_create_user_in_db():
    user: User = await create(payload={
        "name": "Sviatoslav",
        "age": 21,
        "password": "qwerty"
    })

    saved_user: User = await UsersRepository().get(id_=user.id)

    assert saved_user is not None
    assert saved_user == user


async def test_get_users_with_more_than_3_articles(ac: AsyncClient):
    response_token = await ac.post("/token", json={
        "login": "string",
        "password": "string"
    })
    token = response_token.json()['access']

    await ac.post("/users", json={
        "name": "Dima",
        "age": 21,
        "password": "12qwerty"
    }, headers={"Authorization": f"Bearer {token}"})

    for _ in range(5):
        await ac.post("/article", json={
            "text": "Test_1",
            "color": "red",
            "authorId": 1
        }, headers={"Authorization": f"Bearer {token}"})

    for _ in range(2):
        await ac.post("/article", json={
            "text": "Test_2",
            "color": "blue",
            "authorId": 2
        }, headers={"Authorization": f"Bearer {token}"})

    response = await ac.get("/users/unique_names", headers={"Authorization": f"Bearer {token}"})

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == "Sviatoslav"
