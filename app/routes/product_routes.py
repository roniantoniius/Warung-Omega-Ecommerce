from fastapi import (Depends, HTTPException, status, Request, APIRouter)
from tortoise.exceptions import DoesNotExist
from app.models import (Product, user_pydantic, product_pydantic, product_pydanticIn, Category)
from typing import Optional
from datetime import datetime
from starlette.requests import Request
from datetime import date
from app.emails import *
from app.authentication import *
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.post("/products")
async def add_new_product(product: ProductCreate, user: user_pydantic = Depends(get_current_user)):
    product_dict = product.dict()
    
    # Ambil id_category dari data
    category_id = product_dict.pop('id_category')  # Ambil id_category dari dictionary dan hapus dari data
    
    try:
        category = await Category.get(id_category=category_id)
    except Category.DoesNotExist:
        return {"status": "error", "message": "Category not found"}
    
    # Tambahkan id_category ke dalam dictionary produk
    if 'original_price' in product_dict and product_dict['original_price'] > 0:
        product_dict["percentage_discount"] = ((product_dict["original_price"] - product_dict['new_price']) / product_dict['original_price']) * 100


    product_obj = await Product.create(
        **product_dict,
        business=user,
        category=category  
    )
    product_obj = await product_pydantic.from_tortoise_orm(product_obj)
    
    return {"status": "ok", "data": product_obj}

@router.get("/products")
async def get_products():
    response = await product_pydantic.from_queryset(Product.all())
    return {"status": "ok", "data": response}

@router.get("/products-page", response_class=HTMLResponse)
async def products_page(request: Request, page: int = 1, id_category: int = None):
    per_page = 6
    start = (page - 1) * per_page
    end = start + per_page

    # Jika id_category diberikan, filter berdasarkan id_category
    if id_category:
        products = await Product.filter(category_id=id_category).limit(per_page).offset(start)
        total_products = await Product.filter(category_id=id_category).count()
    else:
        products = await Product.all().limit(per_page).offset(start)
        total_products = await Product.all().count()

    total_pages = (total_products + per_page - 1) // per_page
    products_data = [await product_pydantic.from_tortoise_orm(product) for product in products]

    categories = await Category.all()  # Untuk daftar kategori pada sidebar filter

    user = await get_current_user(request)

    if user is None:
        return templates.TemplateResponse("products.jinja", {"request": request,
                                                            "username": None,
                                                            "id_user": None,
                                                            "products": products_data,
                                                            "page": page,
                                                            "total_pages": total_pages,
                                                            "categories": categories,
                                                            "selected_category": id_category})
    
    username = user.username
    id_user = user.id

    return templates.TemplateResponse(
        "products.jinja", 
        {
            "request": request,
            "username": username,
            "products": products_data, 
            "page": page, 
            "total_pages": total_pages, 
            "categories": categories, 
            "selected_category": id_category,  # Untuk mengetahui kategori yang dipilih
            "id_user": id_user
        }
    )

@router.get("/products/{id}")
async def specific_product(id: int):
    product = await Product.get(id=id)
    business = await product.business
    owner = await business.owner
    category = await product.category  # Dapatkan kategori produk
    
    response = await product_pydantic.from_queryset_single(Product.get(id=id))
    
    return {
        "status": "ok",
        "data": {
            "product_details": response,
            "business_details": {
                "name": business.business_name,
                "city": business.city,
                "region": business.region,
                "description": business.business_description,
                "logo": business.logo,
                "owner_id": owner.id,
                "email": owner.email,
                "join_date": owner.join_date.strftime("%b %d %Y")
            },
            "category_details": {
                "id_category": category.id_category,
                "category_name": category.category_name
            }
        }
    }

@router.delete("/products/{id}")
async def delete_product(id: int, user: user_pydantic = Depends(get_current_user)):
    product = await Product.get(id=id)
    business = await product.business
    owner = await business.owner
    if owner == user:
        await product.delete()
        return {"status": "ok"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/products-detail/{id}", response_class=HTMLResponse)
async def product_detail(request: Request, id: int):
    try:
        product = await Product.get(id=id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ambil data business dan category jika dibutuhkan
    business = await product.business
    owner = await business.owner
    category = await product.category

    user = await get_current_user(request)

    if user is None:
        return templates.TemplateResponse("product-detail.jinja", {"request": request,
                                                            "username": None,
                                                            "id_user": None,
                                                            "product": product,
                                                            "business": business,
                                                            "owner": owner,
                                                            "category": category})
    
    username = user.username
    id_user = user.id

    # Return halaman detail produk dengan data produk
    return templates.TemplateResponse(
        "product-detail.jinja", 
        {
            "request": request,
            "username": username,
            "product": product,
            "business": business,
            "owner": owner,
            "category": category,
            "id_user": id_user
        }
    )

@router.put("/product/{id}")
async def update_product(id: int, update_info: product_pydanticIn, user: user_pydantic = Depends(get_current_user)):
    product = await Product.get(id=id)
    business = await product.business
    owner = await business.owner

    # Memperbaiki penulisan 'exclude_unset'
    update_info = update_info.dict(exclude_unset=True)
    update_info["date_published"] = datetime.utcnow()
    
    if user == owner and update_info["original_price"] > 0:
        update_info["percentage_discount"] = ((update_info["original_price"] - update_info['new_price']) / update_info['original_price']) * 100

        # Memperbarui objek produk
        await product.update_from_dict(update_info)
        await product.save()

        response = await product_pydantic.from_tortoise_orm(product)
        return {"status": "ok", "data": response}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated to perform this action or invalid user input",
            headers={"WWW-Authenticate": "Bearer"},
        )