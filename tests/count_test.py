import pytest
from conftest import client


class TestCount:
    @classmethod
    def test_post(cls, menu_params):
        response = client.post(url="api/v1/menus", json=menu_params)
        response_json = response.json()
        cls.id = response_json["id"]
        assert response.status_code == 201
        assert "id" in response_json
        assert response_json["title"] == menu_params["title"]
        assert response_json["description"] == menu_params["description"]

    @classmethod
    def test_get_specified(cls, menu_details):
        response = client.get(url=f"api/v1/menus/{cls.id}")
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["title"] == menu_details["title"]
        assert response_json["description"] == menu_details["description"]

    @classmethod
    def test_get_all(cls, menu_params):
        response = client.get(url=f"api/v1/menus")
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) >= 1
        assert "id" in response_json[0]
        assert response_json[0]["title"] == menu_params["title"]
        assert response_json[0]["description"] == menu_params["description"]

    @classmethod
    def test_patch(cls, menu_update_details):
        response = client.patch(url=f"api/v1/menus/{cls.id}", json=menu_update_details)
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert response_json["title"] == menu_update_details["title"]
        assert response_json["description"] == menu_update_details["description"]

    @classmethod
    def test_delete(cls):
        response = client.delete(url=f"api/v1/menus/{cls.id}")
        assert response.status_code == 200
