from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .routes import routes
from . import title, description, version


api = FastAPI()

for route in routes:
    api.include_router(route)

api.openapi_schema = get_openapi(
    title       = title,
    description = description,
    version     = version,
    routes      = api.routes,
)
