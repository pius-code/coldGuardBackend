from fastapi import APIRouter, HTTPException
from schema.sensor import SensorCreate
from repository.sensor import add_sensor_data
from utils.logger import slogger

router = APIRouter(prefix="/api/v1/sensor", tags=["Sensor readings"])


@router.post("/add_data")
async def add_a_sensor_data(data: SensorCreate):
    slogger.info("Sensor data received")
    slogger.debug(f"Sensor reading: temp={data.temperature}, humidity={data.humidity}, light={data.light_intensity}")
    if not data:
        raise HTTPException(status_code=400, detail="Your data is invalid")
    await add_sensor_data(data)
    return {"status": "success"}
