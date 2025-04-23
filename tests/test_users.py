from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserOut

client = TestClient(app)

def test_root():
    response = client.get("/")
    #print(response.json().get("message"))
    assert response.status_code == 200
    assert response.json() == {"message": "Hello !!!"}


def test_create_user():
    response = client.post("/users/", json={"email": "hello123@gmail.com", "password": "admin"})

    print(response.json())
    new_user = UserOut(**response.json())
    assert new_user.email == "hello123@gmail.com"
    assert response.status_code == 201
