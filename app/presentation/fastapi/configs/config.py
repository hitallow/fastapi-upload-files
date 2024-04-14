import importlib
import os
import threading
import time
from contextlib import asynccontextmanager

import schedule
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.fastapi.middlewares.error_handling_middleware import \
    ErrorHandlingMiddleware


def apply_routes_config(app: FastAPI):
    """
    This function will apply automatically all routes defined in app/presentation/fastapi/routes
    """
    path = os.path.dirname(__file__) + "/../routes/"

    route_definitions = [
        filename.replace(".py", "")
        for filename in os.listdir(path)
        if os.path.isfile(f"{path}{filename}")
        and not filename.startswith("__")
        and filename.endswith(".py")
    ]
    for router in route_definitions:
        try:
            app.include_router(
                importlib.import_module(
                    f"app.presentation.fastapi.routes.{router}"
                ).router
            )
        except Exception:
            pass


def apply_crons():

    path = os.path.dirname(__file__) + "/../crons/"

    crons_registers = [
        filename.replace(".py", "")
        for filename in os.listdir(path)
        if filename.endswith("crons.py")
    ]

    for cron_file in crons_registers:
        try:
            importlib.import_module(
                f"app.presentation.fastapi.crons.{cron_file}"
            ).register()
        except Exception as e:
            print(e)
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    apply_crons()

    watch_crons = True

    def run_scheduler():
        while watch_crons:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=run_scheduler)
    thread.start()

    yield

    watch_crons = False
    schedule.clear()
    time.sleep(2)
    print("parando threads")


def create_app():

    app = FastAPI(
        title="FasAPI Upload",
        description="Upload de arquivos CSV para importação de dados",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(ErrorHandlingMiddleware)

    apply_routes_config(app)

    return app
