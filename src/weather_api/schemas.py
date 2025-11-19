from pydantic import BaseModel


class ResponseSchema(BaseModel):
    message: str


class ReadWeatherRequest(BaseModel):
    location: str


class ReadWeatherResponse(ResponseSchema): ...
