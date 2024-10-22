from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='postgres://<YOUR NAME>:<YOUR SUPABASE IP>:6543/<YOUR DATABASE NAME>',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()