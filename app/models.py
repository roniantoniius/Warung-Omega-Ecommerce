from tortoise import Model
from pydantic import BaseModel
from tortoise import fields
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    id = fields.IntField(pk = True, index = True)
    username = fields.CharField(max_length = 20, null = False, unique = True)
    email = fields.CharField(max_length = 200, null = False, unique = True)
    password = fields.CharField(max_length = 100, null = False)
    phone = fields.CharField(max_length=15, null=False)
    address = fields.TextField(null=True)
    is_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(default = datetime.utcnow)


class Business(Model):
    id = fields.IntField(pk = True, index = True)
    business_name = fields.CharField(max_length = 20, nullable = False, unique = True)
    city = fields.CharField(max_length = 100, null = False, default = "Unspecified")
    region = fields.CharField(max_length = 100, null = False, default = "Unspecified")
    business_description = fields.TextField(null = True)
    logo = fields.CharField(max_length =200, null = False, default = "default.jpg")
    owner = fields.ForeignKeyField('models.User', related_name='business')

class Category(Model):
    id_category = fields.IntField(pk=True, index=True)
    category_name = fields.CharField(max_length=100, null=False, unique=True)  


class Product(Model):
    id = fields.IntField(pk = True, index = True)
    name = fields.CharField(max_length = 100, null = False, index = True)
    category = fields.ForeignKeyField('models.Category', related_name='products')
    original_price = fields.DecimalField(max_digits = 12, decimal_places = 2)
    new_price = fields.DecimalField(max_digits = 12, decimal_places = 2)
    percentage_discount = fields.IntField()
    offer_expiration_date = fields.DateField(default = datetime.utcnow)
    harga_note = fields.CharField(max_length = 100, null = False)
    produk_note = fields.CharField(max_length = 100, null = False)
    lokasi = fields.CharField(max_length = 100, null = False)
    product_description = fields.TextField(null = True)
    tips = fields.TextField(null = True)
    product_image = fields.CharField(max_length =200, null = False, default = "productDefault.jpg")
    date_published = fields.DatetimeField(default = datetime.utcnow)
    business = fields.ForeignKeyField('models.Business', related_name='products')

# Tabel Resep
class Resep(Model):
    id = fields.IntField(pk=True, index=True)
    nama_resep = fields.CharField(max_length=100, null=False)
    gambar_resep = fields.CharField(max_length=200, null=False, default="default_resep.jpg")
    bahan_1 = fields.TextField(null=False)
    bahan_2 = fields.TextField(null=True)
    bahan_3 = fields.TextField(null=True)
    langkah_1 = fields.TextField(null=False)
    langkah_2 = fields.TextField(null=True)
    langkah_3 = fields.TextField(null=True)

class Beli(Model):
    id_beli = fields.IntField(pk=True, index=True)
    user = fields.ForeignKeyField('models.User', related_name='belis', on_delete=fields.CASCADE)
    product = fields.ForeignKeyField('models.Product', related_name='belis', on_delete=fields.CASCADE)
    kuantitas = fields.IntField()
    harga_total = fields.DecimalField(max_digits=12, decimal_places=2)

class Transaksi(Model):
    id_transaksi = fields.IntField(pk=True, index=True)
    user = fields.ForeignKeyField('models.User', related_name='transaksis', on_delete=fields.CASCADE)
    belis = fields.ManyToManyField('models.Beli', related_name='transaksis')
    total = fields.DecimalField(max_digits=12, decimal_places=2)
    status = fields.BooleanField(default=False)
    
class TransaksiDetail(Model):
    id_detail = fields.IntField(pk=True, index=True)
    transaksi = fields.ForeignKeyField('models.Transaksi', related_name='details', on_delete=fields.CASCADE)
    product = fields.ForeignKeyField('models.Product', related_name='transaksi_details', on_delete=fields.CASCADE)
    kuantitas = fields.IntField()
    harga_total = fields.DecimalField(max_digits=12, decimal_places=2)


user_pydantic = pydantic_model_creator(User, name ="User", exclude=("is_verified",))
user_pydanticIn = pydantic_model_creator(User, name = "UserIn", exclude_readonly = True, exclude=("is_verified", 'join_date'))
user_pydanticOut = pydantic_model_creator(User, name = "UserOut", exclude = ("password", ))

business_pydantic = pydantic_model_creator(Business, name = "Business")
business_pydanticIn = pydantic_model_creator(Business, name = "Business", exclude_readonly = True)

category_pydantic = pydantic_model_creator(Category, name = "Category")
category_pydanticIn = pydantic_model_creator(Category, name = "CategoryIn", exclude_readonly = True)

product_pydantic  = pydantic_model_creator(Product, name = "Product")
product_pydanticIn = pydantic_model_creator(Product, name = "ProductIn", exclude = ("percentage_discount", "id", "product_image", "date_published"))

resep_pydantic = pydantic_model_creator(Resep, name="Resep")
resep_pydanticIn = pydantic_model_creator(Resep, name="ResepIn", exclude_readonly= ("id", "gambar_resep"))

beli_pydantic = pydantic_model_creator(Beli, name="Beli")
beli_pydanticIn = pydantic_model_creator(Beli, name="BeliIn", exclude=("id_beli", "user", "harga_total"))

transaksi_pydantic = pydantic_model_creator(Transaksi, name="Transaksi")
transaksi_pydanticIn = pydantic_model_creator(Transaksi, name="TransaksiIn", exclude=("id_transaksi", "user", "belis", "status"))
