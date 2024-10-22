
from fastapi import (Query, APIRouter)

from app.models import (Product, product_pydantic)

router = APIRouter()

@router.get("/search")
async def search_products(query: str = Query(...)):
    response = await product_pydantic.from_queryset(Product.filter(name__icontains=query))
    return {"status": "ok", "data": response}