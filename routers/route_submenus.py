from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from services import service as RestaurantService
from dto import dto_restaurant as RestaurantDTO
from uuid import UUID
from models.models_restaurant import Submenu

router = APIRouter()
database_service = RestaurantService.DbService(Submenu)


@router.post("/{menu_id}/submenus", tags=["submenu_getter"])
async def create_submenu(
    data: RestaurantDTO.Submenu,
    menu_id: UUID,
    db: Session = Depends(get_db),
):
    submenu_creation = database_service.create(db=db, data=data, menu_id=menu_id)
    if not submenu_creation:
        return Response(content="Failed to create menu", status_code=400)
    json_compatible_item_data = jsonable_encoder(submenu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get("/{menu_id}/submenus/{submenu_id}", tags=["specified_menu"])
async def get_value_submenu(submenu_id: UUID, db: Session = Depends(get_db)):
    specified_submenu = database_service.get_value(db, submenu_id)
    if not specified_submenu:
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)
    return specified_submenu


@router.get("/{menu_id}/submenus", tags=["all_submenus"])
async def get_all_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    all_values = database_service.get_all(db, menu_id)
    return all_values


@router.patch("/{menu_id}/submenus/{submenu_id}", tags=["change_submenu_data"])
async def change_submenu_data(
    menu_id: UUID,
    submenu_id: UUID,
    data: RestaurantDTO.Submenu,
    db: Session = Depends(get_db),
):
    update_submenu = database_service.update(db, data, submenu_id)
    json_compatible_item_data = jsonable_encoder(update_submenu)
    return JSONResponse(content=json_compatible_item_data, status_code=200)


@router.delete("/{menu_id}/submenus/{submenu_id}", tags=["delete_submenus"])
async def delete(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    return database_service.remove(db, submenu_id)
