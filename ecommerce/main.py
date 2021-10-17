from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import *
from authentication import (get_hashed_password)

#signal
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient


app = FastAPI()

# creates a business platform for account owner
@post_save(User)
async def create_business(
    sender : "Type[User]", 
    instance : User,
    created : bool,
    using_db : "Optional[BaseDBAsyncClient]", 
    updated_fields: List[str]
) -> None:

    if created:
        business_obj = await Business.create(
            business_name = instance.username, owner = instance
        )

        await business_pydantic.from_tortoise_orm(business_obj)
        #send the email



# User registration route
@app.post("/registration")
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"]) 
    user_obj = await User.create(**user_info)
    new_user = user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status" : "ok",
        "data" : f"Hello {new_user.username}, thanks for choosing our services. Please check your email inbox on the link to confirm your registration."
    }

     

@app.get('/')
def index():
    return {"Message":"Hello"}


# Initializing an sqlite database
register_tortoise(
    app,
    db_url = "sqlite://database.sqlite3",
    modules = {"models":["models"]},
    generate_schemas= True,
    add_exception_handlers = True
)

