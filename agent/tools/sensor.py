from repository.sensor import get_sensor_readings


async def get_the_sensor_readings(days: int):
    readings = await get_sensor_readings(days)
    return readings
