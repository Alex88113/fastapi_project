import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.fastapi.routers.product_router import router as products_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

src = FastAPI()

src.mount("/static", StaticFiles(directory="app/fastapi/static"), name="static")
templates = Jinja2Templates(directory="app/fastapi/frontend")

@src.middleware("http")
async def log_request(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

@src.get("/ui/products")
async def ui_list(request: Request):
    return templates.TemplateResponse(request, "products_list.html")

@src.get("/ui/products/new")
async def ui_new(request: Request):
    return templates.TemplateResponse(request, "product_form.html")

@src.get("/ui/products/edit")
async def ui_edit(request: Request):
    return templates.TemplateResponse(request, "product_form.html")

src.include_router(products_router)
