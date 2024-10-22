from fastapi import (APIRouter)
from app.models import (Category, category_pydantic, category_pydanticIn)

from app.emails import *
from app.authentication import *

router = APIRouter()

@router.get("/categories")
async def get_categories():
    response = await category_pydantic.from_queryset(Category.all())
    return {"status": "ok", "data": response}

@router.get("/categories/{id_category}")
async def get_category_by_id(id_category: int):
    category = await Category.get(id_category=id_category)
    if not category:
        return {"status": "error", "message": "Category not found"}
    
    response = await category_pydantic.from_tortoise_orm(category)
    return {"status": "ok", "data": response}

@router.post("/categories")
async def add_new_category(category: category_pydanticIn):
    category_obj = await Category.create(**category.dict(exclude_unset=True))
    response = await category_pydantic.from_tortoise_orm(category_obj)
    return {"status": "ok", "data": response}

@router.delete("/categories/{id_category}")
async def delete_category(id_category: int):
    category = await Category.get(id_category=id_category)
    if not category:
        return {"status": "error", "message": "Category not found"}
    
    await category.delete()
    return {"status": "ok", "message": "Category deleted successfully"}