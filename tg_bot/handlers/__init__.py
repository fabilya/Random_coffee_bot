from tg_bot.handlers.default import default_router
from tg_bot.handlers.admin import admin_router
from tg_bot.handlers.main_menu import main_menu_router
from tg_bot.handlers.registration import registration_router

all_routers = (
    default_router,
    admin_router,
    main_menu_router,
    registration_router,
)
