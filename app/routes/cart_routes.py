from app.main import templates
from fastapi import (Depends, HTTPException, Request, APIRouter)
from app.models import (User, Product, user_pydantic, Beli, beli_pydantic)
from typing import List
from starlette.requests import Request
from app.emails import *
from app.authentication import *
from fastapi.responses import HTMLResponse

router = APIRouter()

class BeliInput(BaseModel):
    produk_id: int
    kuantitas: int

@router.post("/belis")
async def create_beli(beli_input: BeliInput, user: user_pydantic = Depends(get_current_user)):
    # Retrieve product by ID
    produk = await Product.get(id=beli_input.produk_id)
    if not produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    # Calculate harga_total
    harga_total = produk.new_price * beli_input.kuantitas

    # Create new Beli object
    beli_obj = await Beli.create(
        user_id=user.id,
        product_id=produk.id,
        kuantitas=beli_input.kuantitas,
        harga_total=harga_total
    )

    return {"status": "ok", "data": await beli_pydantic.from_tortoise_orm(beli_obj)}

@router.get("/belis/{username}", response_class=HTMLResponse)
async def get_my_belis(request: Request, username: str):
    user = await User.filter(username=username).first()

    if user is None:
        return templates.TemplateResponse("beli.html", {
            "request": request, 
            "username": None, 
            "id_user": None,
            "client_key": config_credentials["YOUR_MIDTRANS_CLIENT_KEY"]
        })

    id_user = user.id

    belis = await Beli.filter(user=user).select_related('product')

    beli_list = []
    for beli in belis:
        product = beli.product
        beli_data = {
            "beli_id": beli.id_beli,
            "kuantitas": beli.kuantitas,
            "harga_total": beli.harga_total,
            "product": {
                "id": product.id,
                "name": product.name,
                "original_price": product.original_price,
                "new_price": product.new_price,
                "percentage_discount": product.percentage_discount,
                "product_description": product.product_description,
                "product_image": product.product_image,
            }
        }
        beli_list.append(beli_data)
    
    username = user.username

    response = templates.TemplateResponse(
        "beli.html",
        {
            "request": request,
            "beli_list": beli_list,
            "username": username,
            "id_user": id_user,
            "client_key": config_credentials["YOUR_MIDTRANS_CLIENT_KEY"]
        }
    )
    return response

@router.get("/belis/{id_beli}")
async def get_beli_by_id(id_beli: int):
    # Retrieve Beli by ID
    beli = await Beli.get(id_beli=id_beli).select_related('product', 'user')
    if not beli:
        raise HTTPException(status_code=404, detail="Beli tidak ditemukan")

    # Convert to Pydantic model
    beli_details = await beli_pydantic.from_tortoise_orm(beli)

    # Access product details
    product = beli.product 
    user = beli.user

    response_data = {
        "status": "ok",
        "data": {
            "beli_details": beli_details,
            "product": {
                "id": product.id,
                "name": product.name,
                "original_price": product.original_price,
                "new_price": product.new_price,
                "percentage_discount": product.percentage_discount,
                "product_description": product.product_description
            },
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    }

    return response_data

@router.get("/belis", response_model=List[beli_pydantic])
async def get_belis(user: user_pydantic = Depends(get_current_user)):
    belis = await Beli.filter(user=user).select_related('product')
    return belis


@router.delete("/belis/{beli_id}/hapus")
async def hapus_beli(beli_id: int,
                     current_user: User = Depends(get_current_user)):
    beli = await Beli.get(id_beli=beli_id, user_id=current_user.id)
    if not beli:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    await beli.delete()
    return {"status": "ok"}