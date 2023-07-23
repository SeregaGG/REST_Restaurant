from fastapi import FastAPI, APIRouter
from src.menu.router import menu as MenuRouter
from src.submenu.router import submenu as SubmenuRouter
from src.dish.router import dish as DishRouter
from src.database import init_db
from src.menu.models import Menu
from src.submenu.models import Submenu
from src.dish.models import Dish

app = FastAPI()

api = APIRouter(prefix="/api/v1")
api.include_router(
    MenuRouter,
    prefix="/menus",
    tags=["Menu"]
)
api.include_router(
    SubmenuRouter,
    prefix="/menus/{menu_id}/submenus",
    tags=["Submenus"]
)
api.include_router(
    DishRouter,
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dish"]
)
app.include_router(api)


@app.on_event('startup')
async def on_startup():
    await init_db()
