from .route_menus import APIRouter, Depends, Response
from .route_menus import jsonable_encoder, JSONResponse
from .route_menus import Session, get_db
from .route_menus import RestaurantService, RestaurantDTO
from .route_menus import UUID
from models.models_restaurant import Dishes

router = APIRouter()
database_service = RestaurantService.DbService(Dishes)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", tags=["Create"])
async def create_dishes(
    submenu_id: UUID,
    data_dishes: RestaurantDTO.Dishes,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        create_dish_result = database_service.create(
            db=db_session, data=data_dishes, submenu_id=submenu_id
        )
        if not create_dish_result:
            return JSONResponse(content="Failed to create menu", status_code=400)
        json_compatible_item_data = jsonable_encoder(create_dish_result)
        json_compatible_item_data["price"] = str(
            json_compatible_item_data["price"]
        )  # Преобразовать значение 12.50 > '12.50'
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["Read"])
async def get_value_dishes(
    dish_id: UUID,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        specified_dishes = database_service.get_value(db=db_session, id=dish_id)
        if not specified_dishes:
            return JSONResponse(content={"detail": "dish not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=jsonable_encoder(specified_dishes), status_code=200)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes", tags=["Read all"])
async def get_all_dishes(
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        all_values = database_service.get_all(db=db_session)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=jsonable_encoder(all_values))


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["Update"])
async def change_dishes_data(
    dish_id: UUID,
    data_dishes: RestaurantDTO.Dishes,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        update_result = database_service.update(db=db_session, data=data_dishes, id=dish_id)
        json_compatible_item_data = jsonable_encoder(update_result)
        json_compatible_item_data["price"] = str(json_compatible_item_data["price"])
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(content=json_compatible_item_data, status_code=200)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["Delete"])
async def delete_dish(
    dish_id: UUID,
    db_session: Session = Depends(get_db),
) -> JSONResponse:
    try:
        remove_result = database_service.remove(db=db_session, id=dish_id)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
    return JSONResponse(jsonable_encoder(remove_result), status_code=200)
