import pytest
from conftest import client


@pytest.fixture()
def menu_params():
    return {"title": "My menu 1", "description": "My menu description 1"}


@pytest.fixture()
def submenu_params():
    return {"title": "My submenu 1", "description": "My submenu description 1"}


@pytest.fixture()
def dish_params():
    return [
        {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "12.50",
        },
        {
            "title": "My dish 2",
            "description": "My dish description 2",
            "price": "14.50",
        },
    ]


@pytest.mark.usefixtures("menu_params", "submenu_params", "dish_params")
class TestCount:
    @classmethod
    def test_post(cls, menu_params):
        response = client.post(url="api/v1/menus", json=menu_params)
        response_json = response.json()
        cls.menu_id = response_json["id"]
        assert response.status_code == 201
        assert "id" in response_json

    @classmethod
    def test_submenu_create(cls, submenu_params):
        response = client.post(
            url=f"api/v1/menus/{cls.menu_id}/submenus", json=submenu_params
        )
        response_json = response.json()
        cls.submenu_id = response_json["id"]
        assert response.status_code == 201
        assert "id" in response_json
        assert "menu_id" in response_json

    @classmethod
    def test_first_dish_create(cls, dish_params):
        response = client.post(
            url=f"api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes",
            json=dish_params[0],
        )
        response_json = response.json()
        cls.first_dish_id = response_json["id"]
        assert response.status_code == 201
        assert "id" in response_json

    @classmethod
    def test_second_dish_create(cls, dish_params):
        response = client.post(
            url=f"api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes",
            json=dish_params[1],
        )
        response_json = response.json()
        cls.second_dish_id = response_json["id"]
        assert response.status_code == 201
        assert "id" in response_json

    @classmethod
    def test_menu_get_specified(cls):
        response = client.get(url=f"api/v1/menus/{cls.menu_id}")
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["submenus_count"] == 1
        assert response_json["dishes_count"] == 2

    @classmethod
    def test_submenu_get_specified(cls):
        response = client.get(url=f"api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}")
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["dishes_count"] == 2

    @classmethod
    def test_submenu_delete(cls):
        response = client.delete(url=f"api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}")
        assert response.status_code == 200

    @classmethod
    def test_submenu_get_all(cls):
        response = client.get(url=f"api/v1/menus/{cls.menu_id}/submenus")
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []

    @classmethod
    def test_dish_get_all(cls):
        response = client.get(
            url=f"api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes"
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []

    @classmethod
    def test_menu_get_specified_2(cls):
        response = client.get(url=f"api/v1/menus/{cls.menu_id}")
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["submenus_count"] == 0
        assert response_json["dishes_count"] == 0

    @classmethod
    def test_menu_delete(cls):
        response = client.delete(url=f"api/v1/menus/{cls.menu_id}")
        assert response.status_code == 200

    @classmethod
    def test_menu_get_all(cls):
        response = client.get(url=f"api/v1/menus")
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []