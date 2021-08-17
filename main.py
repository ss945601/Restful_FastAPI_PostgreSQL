
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from router import user
app = FastAPI(title = "REST API using FastAPI & PostgreSQL")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router)
