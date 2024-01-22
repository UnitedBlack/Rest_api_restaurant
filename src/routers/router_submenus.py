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


@router.post("/{menu_id}/submenus", tags=["Create"])
async def create_submenu(
    menu_data: RestaurantDTO.Submenu,
    menu_id: UUID,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        create_submenu_result = database_service.create(
            db=db_session, data=menu_data, menu_id=menu_id
        )
        if not create_submenu_result:
            return Response(content="Failed to create menu", status_code=400)
        json_compatible_item_data = jsonable_encoder(create_submenu_result)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get("/{menu_id}/submenus/{submenu_id}", tags=["Read"])
async def get_value_submenu(
    submenu_id: UUID,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        specified_submenu = database_service.get_value(db=db_session, id=submenu_id)
        if not specified_submenu:
            return JSONResponse(
                content={"detail": "submenu not found"}, status_code=404
            )
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=jsonable_encoder(specified_submenu), status_code=200)


@router.get("/{menu_id}/submenus", tags=["Read all"])
async def get_all_submenus(
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        all_values = database_service.get_all(db=db_session)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=jsonable_encoder(all_values))


@router.patch("/{menu_id}/submenus/{submenu_id}", tags=["Update"])
async def change_submenu_data(
    submenu_id: UUID,
    submenu_data: RestaurantDTO.Submenu,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        update_submenu = database_service.update(
            db=db_session, data=submenu_data, id=submenu_id
        )
        json_compatible_item_data = jsonable_encoder(update_submenu)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=json_compatible_item_data, status_code=200)


@router.delete("/{menu_id}/submenus/{submenu_id}", tags=["Delete"])
async def delete_submenu(
    submenu_id: UUID,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        remove_result = database_service.remove(db=db_session, id=submenu_id)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(jsonable_encoder(remove_result), status_code=200)
