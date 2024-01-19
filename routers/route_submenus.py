from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from services import service_menu as RestaurantService
from dto import dto_restaurant as RestaurantDTO
from uuid import UUID
from models.models_restaurant import Submenu

router = APIRouter()
database_service = RestaurantService.DbService()


@router.post("/{id}/submenus", tags=["submenu_getter"])
async def create_submenu(
    data: RestaurantDTO.Submenu,
    id: UUID,
    db: Session = Depends(get_db),
):
    submenu_creation = database_service.create_submenu(data, id, db)
    # print(f"Submenu_creation_result: {submenu_creation}, Data: {data}, Db: {db}")
    if not submenu_creation:
        return Response(content="Failed to create menu", status_code=400)
    json_compatible_item_data = jsonable_encoder(submenu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get("/{menu_id}/submenus/{id}", tags=["specified_menu"])
async def get_value_submenu(menu_id: UUID, id: UUID, db: Session = Depends(get_db)):
    specified_submenu = database_service.get_value_submenu(id, db)
    if not specified_submenu:
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)
    return specified_submenu


@router.get("/{submenu_id}/submenus", tags=["all_submenus"])
async def get_all_submenus(submenu_id: UUID, db: Session = Depends(get_db)):
    return database_service.get_all_submenus(submenu_id, db)


@router.patch("/submenus/{id}", tags=["change_submenu_data"])
async def change_submenu_data(
    id: UUID, data: RestaurantDTO.Submenu, db: Session = Depends(get_db)
):
    update_submenu = database_service.update_submenu(data, db, id)
    json_compatible_item_data = jsonable_encoder(update_submenu)
    return JSONResponse(content=json_compatible_item_data, status_code=200)


@router.delete("/submenus/{id}", tags=["delete_submenus"])
async def delete(id: UUID, db: Session = Depends(get_db)):
    return database_service.remove_submenu(db, id)
