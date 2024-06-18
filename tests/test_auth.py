import pytest
from fastapi import HTTPException
from app.routers.auth import login
from app.models import LoginRequest 
email = "testuser@gmail.com"
mock_password = "1234"

@pytest.mark.asyncio
async def test_login_successful():
    login_data = LoginRequest(email=email, password=mock_password)
    access_token = await login(login_data=login_data)
    
    assert isinstance(access_token["access_token"], str)

@pytest.mark.asyncio
async def test_login_incorrect_credentials():
    login_data = LoginRequest(email=email, password="wrong_password")

    with pytest.raises(HTTPException) as exc_info:
        await login(login_data)
        
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect username or password"
