from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import httpx

from weather_api.schemas import ReadWeatherRequest, ReadWeatherResponse
from weather_api.settings import Settings

settings = Settings() # type: ignore
api_url = settings.WEATHER_API_URL
api_key = settings.WEATHER_API_KEY

router = APIRouter(prefix="/weathers")


@router.get("/", status_code=HTTPStatus.OK)
async def read_location_weather(location: str):
    url = f"{api_url}/{location}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={
                    "unitGroup": "us",
                    "elements": (
                        "remove:cloudcover,"
                        "remove:datetimeEpoch,"
                        "remove:dew,"
                        "remove:feelslikemax,"
                        "remove:feelslikemin,"
                        "remove:moonphase,"
                        "remove:precipcover,"
                        "remove:preciptype,"
                        "remove:pressure,"
                        "remove:snow,"
                        "remove:snowdepth,"
                        "remove:solarenergy,"
                        "remove:solarradiation,"
                        "remove:uvindex,"
                        "remove:visibility,"
                        "remove:winddir,"
                        "remove:windgust"
                    ),
                    "include": "current,alerts",
                    "key": api_key,
                    "contentType": "json",
                },
                timeout=20,
            )


            response.raise_for_status()
            data = response.json()
            result = {
                'status_code': response.status_code,
                'location': data['resolvedAddress'],
                'timezone': data['timezone'],
                'alerts': data['alerts'],
                'currentConditions': data['currentConditions']
            }

            return {"message": result}

    except httpx.HTTPStatusError as exc:
        resp = exc.response

        try:
            data = resp.json()
            msg = data.get("response") or data.get("message") or "Weather API error"
        except Exception:
            msg = resp.text or "Weather API returned invalid response"

        raise HTTPException(
            status_code=resp.status_code,
            detail=msg,
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error fi",
        )
