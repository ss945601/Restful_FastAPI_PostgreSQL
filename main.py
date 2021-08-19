
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from router import users # add router

app = FastAPI(title = "REST API using FastAPI & PostgreSQL")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
routers = [users] # add router
for item in routers:
    app.include_router(item.router)


