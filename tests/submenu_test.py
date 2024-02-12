import pytest
from conftest import client


@pytest.fixture(scope="session", autouse=True)
def get_menu_id():
    menu_params = {"title": "My menu 1", "description": "My menu description 1"}
    response = client.post(url="api/v1/menus", json=menu_params)
    response_json = response.json()
    return response_json["id"]


@pytest.fixture()
def submenu_params():
    return {"title": "My submenu 1", "description": "My submenu description 1"}


@pytest.fixture()
def submenu_details():
    return {
        "id": None,
        "menu_id": None,
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }


@pytest.fixture()
def submenu_update_details():
    return {
        "id": None,
        "menu_id": None,
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
    }


@pytest.mark.usefixtures(
    "submenu_params", "submenu_details", "submenu_update_details", "get_menu_id"
)
class TestSubmenu:
    @classmethod
    def test_submenu_create(cls, submenu_params, get_menu_id):
        response = client.post(
            url=f"api/v1/menus/{get_menu_id}/submenus", json=submenu_params
        )
        response_json = response.json()
        cls.id = response_json["id"]
        assert response.status_code == 201
        assert "id" in response_json
        assert "menu_id" in response_json
        assert response_json["title"] == submenu_params["title"]
        assert response_json["description"] == submenu_params["description"]

    @classmethod
    def test_submenu_get_specified(cls, submenu_details, get_menu_id):
        response = client.get(url=f"api/v1/menus/{get_menu_id}/submenus/{cls.id}")
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["title"] == submenu_details["title"]
        assert response_json["description"] == submenu_details["description"]
        assert response_json["dishes_count"] == 0

    @classmethod
    def test_submenu_get_all(cls, submenu_details, get_menu_id):
        response = client.get(url=f"api/v1/menus/{get_menu_id}/submenus")
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) >= 1
        assert "id" in response_json[0]
        assert response_json[0]["title"] == submenu_details["title"]
        assert response_json[0]["description"] == submenu_details["description"]

    @classmethod
    def test_submenu_update(cls, submenu_update_details, get_menu_id):
        response = client.patch(
            url=f"api/v1/menus/{get_menu_id}/submenus/{cls.id}",
            json=submenu_update_details,
        )
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["title"] == submenu_update_details["title"]
        assert response_json["description"] == submenu_update_details["description"]

    @classmethod
    def test_submenu_delete(cls, get_menu_id):
        response = client.delete(url=f"api/v1/menus/{get_menu_id}/submenus/{cls.id}")
        assert response.status_code == 200
