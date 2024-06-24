from fastapi.testclient import TestClient
from fastapi import status
import pytest
import aiofiles
import os

from ..main import app
from ..settings import settings

client = TestClient(app)

def test_upload_file():
    filename = "valid_file.txt"
    file_content = b"damejoxo@uol.com.br inbox 002200463 size 002142222"
    response = client.put("/", files={"file": (filename, file_content)})

    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT]
    assert response.json() in [settings.response_msg.FILE_STORED, settings.response_msg.FILE_OVERWRITEEN]

def test_upload_file_invalid_filename():
    filename = "invalid_file%$#.txt"
    file_content = b"test content"
    response = client.put("/", files={"file": (filename, file_content)})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": settings.error_msg.FILENAME_NOT_VALID}

def test_list_files():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

def test_get_users_file_not_exists():
    response = client.get("/users/", params={"filename": "non_existent_file.txt"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": settings.error_msg.FILE_NOT_EXISTS}

def test_get_users_invalid_range():
    filename = "valid_file.txt"
    file_content = b"damejoxo@uol.com.br inbox 002200463 size 002142222"
    client.put("/", files={"file": (filename, file_content)})

    response = client.get("/users/", params={"filename": filename, "inbox_range": "100-50"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": settings.error_msg.BAD_RANGE}

def test_upload_file_invalid_data():
    filename = "invalid_data_file.txt"
    file_content = b"invalid data"
    response = client.put("/", files={"file": (filename, file_content)})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": settings.error_msg.INVALID_FILE_CONTENT}

def test_get_users():
    filename = "valid_file.txt"
    file_content = b"damejoxo@uol.com.br inbox 002200463 size 002142222"
    client.put("/", files={"file": (filename, file_content)})

    response = client.get("/users/", params={"filename": filename})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    
    yield

    file_store_path = settings.path.FILE_STORE
    files = os.listdir(file_store_path)

    for file in files:
        os.remove(f"{file_store_path}/{file}")

    os.removedirs(file_store_path)