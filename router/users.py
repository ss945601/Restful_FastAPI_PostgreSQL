
from fastapi import APIRouter,Depends,status
from pydantic import BaseModel
from db_connect import DbConnect
from typing import List,Optional
import sqlalchemy
from datetime import datetime, date

router = APIRouter(
    prefix="/users",
    tags=['users']
)

database, metadata = DbConnect.getDataBase()

users_db = sqlalchemy.Table(
    "users", # table name
    metadata, # db meta
    sqlalchemy.Column('id', primary_key=True),
    sqlalchemy.Column("account"),
    sqlalchemy.Column("password"),
    sqlalchemy.Column("birth")
)    

class usersIn(BaseModel):
    account: str
    password: str
    birth: Optional[datetime]


class users(BaseModel):
    account: str
    password: str
    birth: Optional[datetime]
    id:int


@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@router.get("/", response_model=List[users], status_code = status.HTTP_200_OK)
async def read_users(skip: int = 0, take: int = 20):
    query = users_db.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@router.get("/{id}/", response_model=users, status_code = status.HTTP_200_OK)
async def read_users(id: int):
    query = users_db.select().where(users_db.c.id == id)
    return await database.fetch_one(query)

@router.post("/", response_model=users, status_code = status.HTTP_201_CREATED)
async def create_users(users: usersIn):
    query = users_db.insert().values(account = users.account, password = users.password, birth = users.birth)
    last_record_id = await database.execute(query)
    return {**users.dict(), 'id': last_record_id}

@router.put("/{id}/", response_model=users, status_code = status.HTTP_200_OK)
async def update_users(id: int, users: usersIn):
    query = users_db.update().where(users_db.c.id == id).values(account = users.account, password = users.password, birth = users.birth)
    await database.execute(query)
    return {**users.dict(), 'id': id}    

@router.delete("/{id}/", status_code = status.HTTP_200_OK)
async def remove_users(id: int):
    query = users_db.delete().where(users_db.c.id == id)
    await database.execute(query)
    return {'message':'Delete success'}

