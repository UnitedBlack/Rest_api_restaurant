import pytest
from conftest import client


@pytest.fixture(scope="session")
def get_menu_id():
    menu_params = {"title": "My menu 1", "description": "My menu description 1"}
    response = client.post(url="api/v1/menus", json=menu_params)
    response_json = response.json()
    return response_json["id"]


@pytest.fixture(scope="session")
def get_submenu_id(get_menu_id):
    submenu_params = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = client.post(
        url=f"api/v1/menus/{get_menu_id}/submenus", json=submenu_params
    )
    response_json = response.json()
    return response_json["id"]


@pytest.fixture()
def dish_params():
    return {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
    }


@pytest.fixture()
def dish_details():
    return {
        "title": "My dis232323h 1",
        "description": "My 23di2233sh description 1",
        "price": "12.50",
        "id": "2d0cb675-b282-4753-9180-af7c712066ac",
        "submenu_id": "920d4c11-6562-47a4-bdf8-062fd20609df",
    }


@pytest.fixture()
def dish_update_details():
    return {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50",
    }


@pytest.mark.usefixtures(
    "dish_params",
    "dish_details",
    "dish_update_details",
    "get_menu_id",
    "get_submenu_id",
)
class TestDish:
    @classmethod
    def test_dish_create(cls, dish_params, get_menu_id, get_submenu_id):
        response = client.post(
            url=f"api/v1/menus/{get_menu_id}/submenus/{get_submenu_id}/dishes",
            json=dish_params,
        )
        response_json = response.json()
        cls.id = response_json["id"]
        assert response.status_code == 201
        assert "id" in response_json
        assert "submenu_id" in response_json
        assert response_json["title"] == dish_params["title"]
        assert response_json["description"] == dish_params["description"]
        assert response_json["price"] == dish_params["price"]

    @classmethod
    def test_dish_get_specified(cls, dish_params, get_menu_id, get_submenu_id):
        response = client.get(
            url=f"api/v1/menus/{get_menu_id}/submenus/{get_submenu_id}/dishes/{cls.id}"
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert "submenu_id" in response_json
        assert response_json["title"] == dish_params["title"]
        assert response_json["description"] == dish_params["description"]
        assert response_json["price"] == dish_params["price"]

    @classmethod
    def test_dish_get_all(cls, get_menu_id, get_submenu_id):
        response = client.get(
            url=f"api/v1/menus/{get_menu_id}/submenus/{get_submenu_id}/dishes"
        )
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) >= 1

    @classmethod
    def test_dish_update(cls, dish_update_details, get_menu_id, get_submenu_id):
        response = client.patch(
            url=f"api/v1/menus/{get_menu_id}/submenus/{get_submenu_id}/dishes/{cls.id}",
            json=dish_update_details,
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["title"] == dish_update_details["title"]
        assert response_json["description"] == dish_update_details["description"]

    @classmethod
    def test_dish_delete(cls, get_menu_id, get_submenu_id):
        response = client.delete(
            url=f"api/v1/menus/{get_menu_id}/submenus/{get_submenu_id}/dishes/{cls.id}"
        )
        assert response.status_code == 200
