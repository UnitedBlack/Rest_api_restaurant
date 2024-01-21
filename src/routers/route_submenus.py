from .route_menus import APIRouter, Depends, Response
from .route_menus import jsonable_encoder, JSONResponse
from .route_menus import Session, get_db
from .route_menus import RestaurantService, RestaurantDTO
from .route_menus import UUID
from models.models_restaurant import Submenu

router = APIRouter()
database_service = RestaurantService.DbService(Submenu)


@router.post("/{menu_id}/submenus", tags=["Create"])
async def create_submenu(
    menu_data: RestaurantDTO.Submenu,
    menu_id: UUID,
    db_session: Session = Depends(get_db),
):
    submenu_creation = database_service.create(
        db=db_session, data=menu_data, menu_id=menu_id
    )
    if not submenu_creation:
        return Response(content="Failed to create menu", status_code=400)
    json_compatible_item_data = jsonable_encoder(submenu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get("/{menu_id}/submenus/{submenu_id}", tags=["Read"])
async def get_value_submenu(
    submenu_id: UUID,
    db_session: Session = Depends(get_db),
):
    specified_submenu = database_service.get_value(db=db_session, id=submenu_id)
    if not specified_submenu:
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)
    return specified_submenu


@router.get("/{menu_id}/submenus", tags=["Read all"])
async def get_all_submenus(
    menu_id: UUID,
    db_session: Session = Depends(get_db),
):
    return database_service.get_all(db=db_session, id=menu_id)


@router.patch("/{menu_id}/submenus/{submenu_id}", tags=["Update"])
async def change_submenu_data(
    submenu_id: UUID,
    submenu_data: RestaurantDTO.Submenu,
    db_session: Session = Depends(get_db),
):
    update_submenu = database_service.update(
        db=db_session, data=submenu_data, id=submenu_id
    )
    json_compatible_item_data = jsonable_encoder(update_submenu)
    return JSONResponse(content=json_compatible_item_data, status_code=200)


@router.delete("/{menu_id}/submenus/{submenu_id}", tags=["Delete"])
async def delete_submenu(
    submenu_id: UUID,
    db_session: Session = Depends(get_db),
):
    return database_service.remove(db=db_session, id=submenu_id)
