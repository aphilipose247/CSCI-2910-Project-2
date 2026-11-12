from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import operators
from app.scripts.populate_db import populate

# Uvicorn is the server that our API works on, and FastAPI talks to your database, checks passwords, processes calculations, and sends raw data (usually in JSON format) back to the frontend
@asynccontextmanager
async def lifespan(app: FastAPI):
    populate()
    yield


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


app = FastAPI(
    title="MW4 Operators API",
    description="A REST API for MW Operators in MW 2026.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(operators.router)
