import uuid
import pytest


async def register_and_login(client):
    email = f"user_{uuid.uuid4().hex}@example.com"
    password = "123456"

    register_response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 200

    login_response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


@pytest.mark.asyncio
async def test_create_task(client):
    headers = await register_and_login(client)

    response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test task",
            "description": "Test description",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test task"
    assert data["description"] == "Test description"


@pytest.mark.asyncio
async def test_get_tasks(client):
    headers = await register_and_login(client)

    await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Task 1",
            "description": "Description 1",
        },
    )

    response = await client.get(
        "/tasks",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_update_task(client):
    headers = await register_and_login(client)

    create_response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Old task",
            "description": "Old description",
        },
    )

    task_id = create_response.json()["id"]

    update_response = await client.patch(
        f"/tasks/{task_id}",
        headers=headers,
        json={
            "title": "Updated task",
            "status": "done",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["title"] == "Updated task"
    assert data["status"] == "done"


@pytest.mark.asyncio
async def test_delete_task(client):
    headers = await register_and_login(client)

    create_response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Task to delete",
            "description": "Delete me",
        },
    )

    task_id = create_response.json()["id"]

    delete_response = await client.delete(
        f"/tasks/{task_id}",
        headers=headers,
    )

    assert delete_response.status_code == 200