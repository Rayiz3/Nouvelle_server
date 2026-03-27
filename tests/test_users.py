def test_get_users(users_client):
    response = users_client.get("/users")

    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["name"] == "DevUser"
    assert data[0]["email"] == "dev@test.com"
    assert data[1]["name"] == "ArtistUser"

def test_add_user(users_client):
    response = users_client.post("/users", json={
        "email": "testuser@test.com",
        "password": "testpassword",
        "name": "testuser",
    })

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "User created successful"
    assert data["user"]["email"] == "testuser@test.com"
    assert data["user"]["name"] == "testuser"

def test_get_user(users_client):
    response = users_client.get("/user", query_string={"email": "dev@test.com"})

    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "DevUser"
    assert data["email"] == "dev@test.com"

    response = users_client.get("/user", query_string={"id": data["_id"]})

    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "DevUser"
    assert data["email"] == "dev@test.com"

def test_set_config(users_client, users_collection):
    response = users_client.patch("/user/config",
        query_string={"id": str(users_collection._data[0]["_id"])},
        json={
            "color": "#e74c3c",
            "stacks": ["react", "nodejs"],
            "links": [
                "https://velog.io/@devlog",
            ]
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["config"]["color"] == "#e74c3c"
    assert data["config"]["stacks"] == ["react", "nodejs"]
    assert data["config"]["links"] == ["https://velog.io/@devlog"]