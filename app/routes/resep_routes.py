from fastapi import (HTTPException, status, Request, APIRouter)
from tortoise.exceptions import DoesNotExist
from app.models import (Resep, resep_pydantic, resep_pydanticIn)
from starlette.requests import Request
from app.emails import *
from app.authentication import *
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.post("/reseps")
async def add_new_resep(resep: resep_pydanticIn):
    resep_info = resep.dict(exclude_unset=True)
    resep_obj = await Resep.create(**resep_info)
    resep_obj = await resep_pydantic.from_tortoise_orm(resep_obj)
    return {"status": "ok", "data": resep_obj}

# Get all reseps
@router.get("/reseps")
async def get_reseps():
    response = await resep_pydantic.from_queryset(Resep.all())
    return {"status": "ok", "data": response}

@router.get("/reseps-page", response_class=HTMLResponse)
async def reseps_page(request: Request, page: int = 1):
    user = await get_current_user(request)
    username = user.username
    id_user = user.id

    per_page = 6  # Jumlah item per halaman
    start = (page - 1) * per_page
    end = start + per_page

    # Ambil semua resep dan hitung total resep
    reseps = await Resep.all().limit(per_page).offset(start)
    total_reseps = await Resep.all().count()

    # Hitung total halaman
    total_pages = (total_reseps + per_page - 1) // per_page
    reseps_data = [await resep_pydantic.from_tortoise_orm(resep) for resep in reseps]

    return templates.TemplateResponse(
        "resep.jinja",
        {
            "request": request,
            "username": username,
            "reseps": reseps_data,
            "page": page,
            "total_pages": total_pages,
            "id_user": id_user
        }
    )

@router.get("/reseps-detail/{id}", response_class=HTMLResponse)
async def resep_detail(request: Request, id: int):
    user = await get_current_user(request)
    username = user.username
    id_user = user.id

    try:
        resep = await Resep.get(id=id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Resep was not found")
    
    return templates.TemplateResponse(
        "resep-detail.jinja",
        {
            "request": request,
            "username": username,
            "resep": resep,
            "id_user": id_user
        }
    )

@router.get("/reseps/{id}")
async def get_resep_by_id(id: int):
    try:
        resep = await Resep.get(id=id)
        response = await resep_pydantic.from_tortoise_orm(resep)
        return {"status": "ok", "data": response}
    except Resep.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resep not found",
        )

@router.delete("/reseps/{id}")
async def delete_resep(id: int):
    resep = await Resep.get(id=id)
    await resep.delete()
    return {"status": "ok"}