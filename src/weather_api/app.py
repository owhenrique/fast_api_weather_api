from fastapi import FastAPI
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware

from .schemas import ResponseSchema
from .routers import weather

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router)


@app.get("/", response_model=ResponseSchema, status_code=HTTPStatus.OK)
async def index():
    return {"message": "welcome to the weather api v1."}
