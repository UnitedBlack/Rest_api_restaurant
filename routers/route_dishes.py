from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from services import service as RestaurantService
from dto import dto_restaurant as RestaurantDTO
from uuid import UUID
from models.models_restaurant import Dishes

router = APIRouter()
database_service = RestaurantService.DbService(Dishes)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", tags=["dishes_getter"])
async def create_dishes(
    submenu_id: UUID,
    data: RestaurantDTO.Dishes,
    db: Session = Depends(get_db),
):
    dishes_creation = database_service.create(db, data, submenu_id=submenu_id)
    if not dishes_creation:
        return Response(content="Failed to create menu", status_code=400)
    json_compatible_item_data = jsonable_encoder(dishes_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["specified_menu"]
)
async def get_value_dishes(
    dish_id: UUID,
    db: Session = Depends(get_db),
):
    specified_dishes = database_service.get_value(db, dish_id)
    if not specified_dishes:
        return JSONResponse(content={"detail": "dishes not found"}, status_code=404)
    return specified_dishes


@router.get("/{menu_id}/submenus/{submenu_id}/dishes", tags=["all_dishes"])
async def get_all_dishess(
    submenu_id: UUID,
    db: Session = Depends(get_db),
):
    return database_service.get_all(db, submenu_id)


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["change_dishes_data"]
)
async def change_dishes_data(
    dish_id: UUID,
    data: RestaurantDTO.Dishes,
    db: Session = Depends(get_db),
):
    update_dishes = database_service.update(db, data, dish_id)
    json_compatible_item_data = jsonable_encoder(update_dishes)
    return JSONResponse(content=json_compatible_item_data, status_code=200)


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["delete_dishes"]
)
async def delete(
    dish_id: UUID,
    db: Session = Depends(get_db),
):
    return database_service.remove(db, dish_id)
