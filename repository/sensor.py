from model.sensor import Sensor
from schema.sensor import SensorCreate
from datetime import datetime, timezone, timedelta


# NOTE: All sensor readings are stored in a single global collection with no project/device
# association. This works for single-device deployments, but if multiple devices are ever
# added, their readings will be mixed together and the agent will make incorrect assessments.
# Fix: add a `device_id` or `project_id` field to SensorCreate and filter queries by it.
async def add_sensor_data(data: SensorCreate):
    new_sensor = Sensor(
        dateTime=datetime.now(timezone.utc),
        temperature=data.temperature,
        humidity=data.humidity,
        light_intensity=data.light_intensity,
    )
    await new_sensor.insert()
    return 1


async def get_sensor_readings(days: int):
    from_date = datetime.now() - timedelta(days)
    readings = await Sensor.find(
        Sensor.dateTime >= from_date
        ).sort(Sensor.dateTime).to_list()
    return readings
