import uuid

import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    email = f"user_{uuid.uuid4().hex}@example.com"

    response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == email
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.asyncio
async def test_login_user(client):
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

    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_me(client):
    email = f"user_{uuid.uuid4().hex}@example.com"
    password = "123456"

    await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    login_response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == email
