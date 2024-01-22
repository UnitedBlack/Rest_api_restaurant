import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers import router_menus as MenuRouter
from routers import router_submenus as SubmenuRouter
from routers import router_dishes as DishesRouter
from sqlalchemy.exc import OperationalError
import time

app = FastAPI()
app.include_router(MenuRouter.router, prefix="/api/v1")
app.include_router(SubmenuRouter.router, prefix="/api/v1/menus")
app.include_router(DishesRouter.router, prefix="/api/v1/menus")

if __name__ == "__main__":
    while True:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            print("Waiting for DB")
            time.sleep(1)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=3)
