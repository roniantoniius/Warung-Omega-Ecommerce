from fastapi import (Request, APIRouter)

from app.models import (Product, product_pydantic,)
from starlette.requests import Request
from app.emails import *
from app.authentication import *
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Mengambil 6 produk dari database sebagai objek model ORM
    products = await Product.all().limit(6).order_by("id")
    products_data = [await product_pydantic.from_tortoise_orm(product) for product in products]  # Proses per item

    user = await get_current_user(request)
    
    # Check if user is None and handle the login logic
    if user is None:
        return templates.TemplateResponse("index.jinja", {"request": request,
                                                         "products": products_data,
                                                         "username": None,
                                                         "id_user": None})
    
    username = user.username
    id_user = user.id
    
    return templates.TemplateResponse("index.jinja", {"request": request,
                                                     "products": products_data,
                                                     "username": username,
                                                     "id_user": id_user})