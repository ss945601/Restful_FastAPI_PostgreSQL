
#### build setting ####

table_name = "users"
primaryKeyName = "id" # primary key
primaryKeyType = "int"
optional = "	optional"
# no primary key in inputData
inputData = f"""
account	varchar
password	varchar
birth	timestamp{optional}
"""

#### build setting ####


def TypeConvert(inputType):
    return {
        'varchar': 'str',
        'int': 'int',
        'timestamp': 'datetime',
        'smallint':'int'
    }.get(inputType,'str') 

cols = inputData.split("\n")
sqlalchemyCols = f"    sqlalchemy.Column('{primaryKeyName}', primary_key=True),\n"
classStr = f"class {table_name}In(BaseModel):\n"
valStr = ""
for col in cols:
    if col != "":
        name = col.split("	")[0]
        typename = col.split("	")[1]
        allownull = False
        valStr += f"{name} = {table_name}.{name}, "
        if len(col.split("	")) > 2:
            allownull = True if col.split("	")[2]== "optional" else False
        if allownull:
            classStr += f"    {name}: Optional[{TypeConvert(typename)}]\n"
        else:
            classStr += f"    {name}: {TypeConvert(typename)}\n"
        sqlalchemyCols += f"""    sqlalchemy.Column("{name}"),\n"""
valStr = valStr[:-2]
sqlalchemyCols = sqlalchemyCols[:-2]

pageStr = f"""
from fastapi import APIRouter,Depends,status
from pydantic import BaseModel
from db_connect import DbConnect
from typing import List,Optional
import sqlalchemy
from datetime import datetime, date

router = APIRouter(
    prefix="/{table_name}",
    tags=['{table_name}']
)

database, metadata = DbConnect.getDataBase()

{table_name+"_db"} = sqlalchemy.Table(
    "{table_name}", # table name
    metadata, # db meta
{sqlalchemyCols}
)    

{classStr}

{classStr.replace("In(BaseModel)","(BaseModel)") + f"    {primaryKeyName}:{primaryKeyType}"}
@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@router.get("/", response_model=List[{table_name}], status_code = status.HTTP_200_OK)
async def read_{table_name}(skip: int = 0, take: int = 20):
    query = {table_name+"_db"}.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@router.get("/{"{"+primaryKeyName+"}"}/", response_model={table_name}, status_code = status.HTTP_200_OK)
async def read_{table_name}({primaryKeyName}: int):
    query = {table_name+"_db"}.select().where({table_name+"_db"}.c.{primaryKeyName} == {primaryKeyName})
    return await database.fetch_one(query)

@router.post("/", response_model={table_name}, status_code = status.HTTP_201_CREATED)
async def create_{table_name}({table_name}: {table_name}In):
    query = {table_name+"_db"}.insert().values({valStr})
    last_record_{primaryKeyName} = await database.execute(query)
    return {"{**"}{table_name}{".dict(), '"}{primaryKeyName}{"': last_record_"}{primaryKeyName+"}"}

@router.put("/{"{"+primaryKeyName+"}"}/", response_model={table_name}, status_code = status.HTTP_200_OK)
async def update_{table_name}({primaryKeyName}: int, {table_name}: {table_name}In):
    query = {table_name+"_db"}.update().where({table_name+"_db"}.c.{primaryKeyName} == {primaryKeyName}).values({valStr})
    await database.execute(query)
    return {"{**"}{table_name}{".dict(), '"}{primaryKeyName}': {primaryKeyName+"}"}    

@router.delete("/{"{"+primaryKeyName+"}"}/", status_code = status.HTTP_200_OK)
async def remove_{table_name}({primaryKeyName}: int):
    query = {table_name+"_db"}.delete().where({table_name+"_db"}.c.{primaryKeyName} == {primaryKeyName})
    await database.execute(query)
    return {"{'message':'Delete success'}"}

"""

f = open(__file__.replace("buildModel.py","router/")+table_name+".py", "w")
f.write(pageStr)
f.close()