import pytest
from conftest import client


@pytest.fixture()
def menu_params():
    return {"title": "My menu 1", "description": "My menu description 1"}


@pytest.fixture()
def menu_details():
    return {
        "id": "",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0,
    }


@pytest.fixture()
def update_menu_details():
    return {
        "id": None,
        "description": "My updated menu description 1",
        "title": "My updated menu 1",
    }


@pytest.fixture()
def menu_update_details():
    return {
        "title": "My updated menu 1",
        "id": "e47cc8b0-1f1c-4672-8496-63ff19e2666a",
        "description": "My updated menu description 1",
    }


@pytest.mark.usefixtures("menu_params", "menu_details", "menu_update_details")
class TestMenu:
    @classmethod
    def test_menu_create(cls, menu_params):
        response = client.post(url="api/v1/menus", json=menu_params)
        response_json = response.json()
        cls.id = response_json["id"]
        assert response.status_code == 201
        assert "id" in response_json
        assert response_json["title"] == menu_params["title"]
        assert response_json["description"] == menu_params["description"]

    @classmethod
    def test_menu_get_specified(cls, menu_details):
        response = client.get(url=f"api/v1/menus/{cls.id}")
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["title"] == menu_details["title"]
        assert response_json["description"] == menu_details["description"]

    @classmethod
    def test_menu_get_all(cls, menu_params):
        response = client.get(url=f"api/v1/menus")
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) >= 1
        assert "id" in response_json[0]
        assert response_json[0]["title"] == menu_params["title"]
        assert response_json[0]["description"] == menu_params["description"]

    @classmethod
    def test_menu_update(cls, menu_update_details):
        response = client.patch(url=f"api/v1/menus/{cls.id}", json=menu_update_details)
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["title"] == menu_update_details["title"]
        assert response_json["description"] == menu_update_details["description"]

    @classmethod
    def test_menu_delete(cls):
        response = client.delete(url=f"api/v1/menus/{cls.id}")
        assert response.status_code == 200

# [
#     {
#         "id": None,
#         "title": "My menu 2",
#         "description": "My menu description 2",
#         "submenus_count": 0,
#         "dishes_count": 0,
#     }
# ],
# [
#     {
#         "id": None,
#         "title": "My menu 3",
#         "description": "My menu description 3",
#         "submenus_count": 0,
#         "dishes_count": 0,
#     }
# ],
