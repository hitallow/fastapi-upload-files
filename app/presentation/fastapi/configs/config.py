import importlib
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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


def create_app():

    app = FastAPI(title="Kanastra Upload", description="Upload de arquivos CSV")

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    apply_routes_config(app)

    return app
