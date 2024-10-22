from fastapi import (UploadFile, File, Depends, HTTPException, status, Request, APIRouter)
from app.models import (Product, user_pydantic, Resep)
from starlette.requests import Request
from fastapi import File, UploadFile
import secrets
from PIL import Image

router = APIRouter()

@router.post("/uploadfile/product/{id}")
async def create_upload_file(
    id: int,
    file: UploadFile = File(...),
    user: user_pydantic = Depends(get_current_user),
    request: Request  # Menambahkan parameter request
):
    FILEPATH = "./static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["jpg", "png"]:
        return {"status" : "error", "detail" : "file extension not allowed"}

    token_name = secrets.token_hex(10)+"."+extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size = (200,200))
    img.save(generated_name)

    file.close()
    product = await Product.get(id = id)
    business = await product.business
    owner = await business.owner

    if owner == user:
        product.product_image = token_name
        await product.save()
    
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Not authenticated to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    base_url = f"{request.url.scheme}://{request.url.hostname}"
    if request.url.port:
        base_url += f":{request.url.port}"

    file_url = f"{base_url}/static/images/{token_name}"  # Menggunakan base_url yang dinamis
    return {"status": "ok", "filename": file_url}

    file_url = "localhost:8000" + generated_name[1:]
    return {"status": "ok", "filename": file_url}

@router.post("/uploadfile/resep/{id}")
async def upload_resep_image(id: int, file: UploadFile = File(...), user: user_pydantic = Depends(get_current_user)):
    FILEPATH = "./static/images/"
    filename = file.filename
    extension = filename.split(".")[-1]

    if extension not in ["jpg", "png"]:
        return {"status": "error", "detail": "file extension not allowed"}

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()
    with open(generated_name, "wb") as f:
        f.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    file.close()
    try:
        resep = await Resep.get(id=id)
        if user.is_authenticated:
            resep.gambar_resep = token_name
            await resep.save()
            file_url = "localhost:8000" + generated_name[1:]
            return {"status": "ok", "filename": file_url}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated to perform this action",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Resep.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resep not found",
        )