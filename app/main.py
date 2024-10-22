from app.routes.user_routes import router as user_router
from app.routes.contact_routes import router as contact_router
from app.routes.categories_routes import router as categories_router
from app.routes.search_routes import router as search_router
from app.routes.index_routes import router as index_router
from app.routes.product_routes import router as product_router
from app.routes.resep_routes import router as resep_router
from app.routes.cart_routes import router as cart_router
from app.routes.transaction_routes import router as transaction_router
from app.routes.midtrans_routes import router as midtrans_router
from app.routes.upload_image_routes import router as upload_image_router


from database.db import init_db
from fastapi import FastAPI
from app.models import *

from tortoise import Tortoise
from fastapi.security import OAuth2PasswordBearer
from app.emails import *
from app.authentication import *

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import midtransclient
from dotenv import load_dotenv
import os

app = FastAPI(
    title="Warung Omega API: E-commerce Seafood Restaurant",
    version="3.14"
)

load_dotenv()

MIDTRANS_SERVER_KEY = os.environ.get('YOUR_MIDTRANS_SERVER_KEY')
MIDTRANS_CLIENT_KEY = os.environ.get('YOUR_MIDTRANS_CLIENT_KEY')

midtrans_core_api = midtransclient.CoreApi(
    is_production=False, 
    server_key=MIDTRANS_SERVER_KEY, 
    client_key=MIDTRANS_CLIENT_KEY  
)

snap = midtransclient.Snap(
    is_production=False, 
    server_key=MIDTRANS_SERVER_KEY, 
    client_key=MIDTRANS_CLIENT_KEY  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

async def get_db_connection():
    return await Tortoise.get_connection("default")

oath2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

templates = Jinja2Templates(directory="templates")

app.include_router(user_router)
app.include_router(contact_router)
app.include_router(categories_router)
app.include_router(search_router)
app.include_router(index_router)
app.include_router(product_router)
app.include_router(resep_router)
app.include_router(cart_router)
app.include_router(transaction_router)
app.include_router(midtrans_router)
app.include_router(upload_image_router)


@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()