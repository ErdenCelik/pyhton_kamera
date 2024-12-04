from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

from config.settings import SettingsManager
from src.database.database_manager import DatabaseManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm originlere izin ver
    allow_credentials=True,  # Credentials'a izin ver
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm headerlara izin ver
    expose_headers=["*"],  # Tüm headerları expose et
    max_age=3600,  # Önbellek süresi
)

# Ya da daha basit bir yöntem olarak, özel bir CORS middleware ekle
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Max-Age"] = "3600"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

db_manager = DatabaseManager()
setting_manager = SettingsManager(db_manager=db_manager)

@app.get("/api/detection/{detection_uuid}", response_class=FileResponse)
async def getDetectionImage(detection_uuid: str):
    image = db_manager.db_get_detection_path(detection_uuid)

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    if not os.path.exists(image):
        raise HTTPException(status_code=404, detail="Image file not found")

    return FileResponse(
        image,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        })

@app.get("/api/detection-object/{object_uuid}", response_class=FileResponse)
async def getDetectionObjectImage(object_uuid: str):
    image = db_manager.db_get_detection_object_path(object_uuid)

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    if not os.path.exists(image):
        raise HTTPException(status_code=404, detail="Image file not found")

    return FileResponse(
        image,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

if __name__ == "__main__":

    all_settings = setting_manager.get_all_settings()

    uvicorn.run(app, host="0.0.0.0", port=all_settings['apiPort'])