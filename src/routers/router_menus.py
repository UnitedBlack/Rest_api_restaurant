from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from services import service as RestaurantService
from dto import dto_restaurant as RestaurantDTO
from uuid import UUID
from models.models_restaurant import Menu
from database import metadata
router = APIRouter()
database_service = RestaurantService.DbService(Menu)


@router.post("/menus", tags=["Create"])
async def create_menu(
    data_menu: RestaurantDTO.Menu = None,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        create_menu_result = database_service.create(db=db_session, data=data_menu)
        print(f"METADATA: {metadata.tables}")
        if not create_menu_result:
            return Response(content="Failed to create menu", status_code=400)
        json_compatible_item_data = jsonable_encoder(create_menu_result)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get("/menus/{menu_id}", tags=["Read"])
async def get_menu(
    menu_id: UUID,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        specified_menu = database_service.get_value(db=db_session, id=menu_id)
        if not specified_menu:
            return JSONResponse(content={"detail": "menu not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=jsonable_encoder(specified_menu), status_code=200)


@router.get("/menus", tags=["Read all"])
async def get_all_menus(db_session: Session = Depends(get_db)) -> JSONResponse:
    try:
        all_values = database_service.get_all(db=db_session)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=jsonable_encoder(all_values))


@router.patch("/menus/{menu_id}", tags=["Update"])
async def change_menu_data(
    menu_id: UUID,
    data_menu: RestaurantDTO.Menu = None,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        update_result = database_service.update(
            db=db_session, data=data_menu, id=menu_id
        )
        json_compatible_item_data = jsonable_encoder(update_result)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=json_compatible_item_data, status_code=200)


@router.delete("/menus/{menu_id}", tags=["Delete"])
async def delete(
    menu_id: UUID,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        remove_result = database_service.remove(db=db_session, id=menu_id)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(jsonable_encoder(remove_result), status_code=200)
