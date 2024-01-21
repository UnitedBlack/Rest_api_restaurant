from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from services import service as RestaurantService
from dto import dto_restaurant as RestaurantDTO
from uuid import UUID
from models.models_restaurant import Menu

router = APIRouter()
database_service = RestaurantService.DbService(Menu)


@router.post("/menus", tags=["Create"])
async def create_menu(
    data: RestaurantDTO.Menu = None,
    db: Session = Depends(get_db),
):
    menu_creation = database_service.create(db, data)
    if not menu_creation:
        return Response(content="Failed to create menu", status_code=400)
    json_compatible_item_data = jsonable_encoder(menu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get("/menus/{menu_id}", tags=["Read"])
async def get_menu(
    menu_id: UUID,
    db: Session = Depends(get_db),
):
    specified_menu = database_service.get_value(db, menu_id)
    if not specified_menu:
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)
    return specified_menu


@router.get("/menus", tags=["Read all"])
async def get_all_menus(db: Session = Depends(get_db)):
    return database_service.get_all(db)


@router.patch("/menus/{menu_id}", tags=["Update"])
async def change_menu_data(
    menu_id: UUID,
    data: RestaurantDTO.Menu = None,
    db: Session = Depends(get_db),
):
    update_menu = database_service.update(db, data, menu_id)
    json_compatible_item_data = jsonable_encoder(update_menu)
    return JSONResponse(content=json_compatible_item_data, status_code=200)


@router.delete("/menus/{menu_id}", tags=["Delete"])
async def delete(
    menu_id: UUID,
    db: Session = Depends(get_db),
):
    return database_service.remove(db, menu_id)
