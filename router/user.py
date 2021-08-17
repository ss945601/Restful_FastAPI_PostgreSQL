
from fastapi import APIRouter,Depends,status
from pydantic import BaseModel
from db_connect import DbConnect
from typing import List
import sqlalchemy

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

database, metadata = DbConnect.getDataBase()

users = sqlalchemy.Table(
    "user_repo", # table name
    metadata, # db meta
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True), 
    sqlalchemy.Column("account", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)


class UserIn(BaseModel):
    account: str
    password: str

class User(BaseModel):
    id: int
    account: str
    password: str
    

@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@router.get("/", response_model=List[User], status_code = status.HTTP_200_OK)
async def read_users(skip: int = 0, take: int = 20):
    query = users.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@router.get("/{user_id}/", response_model=User, status_code = status.HTTP_200_OK)
async def read_users(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

@router.post("/", response_model=User, status_code = status.HTTP_201_CREATED)
async def create_user(user: UserIn):
    query = users.insert().values(account=user.account, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@router.put("/{user_id}/", response_model=User, status_code = status.HTTP_200_OK)
async def update_user(user_id: int, payload: UserIn):
    query = users.update().where(users.c.id == user_id).values(account=payload.account, password=payload.password)
    await database.execute(query)
    return {**payload.dict(), "id": user_id}

@router.delete("/{user_id}/", status_code = status.HTTP_200_OK)
async def remove_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User with id: {} deleted successfully!".format(user_id)}
