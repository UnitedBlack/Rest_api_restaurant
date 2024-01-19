import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers import route_menus as MenuRouter
from routers import route_submenus as SubmenuRouter
from routers import route_dishes as DishesRouter

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(MenuRouter.router, prefix="/api/v1")
app.include_router(SubmenuRouter.router, prefix="/api/v1/menus")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=3)
