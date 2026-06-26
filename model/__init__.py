from model.user import User
from model.project import Project
from model.asha_device import AshaDevice
from model.sensor import Sensor

__all__ = ["User", "Project", "Sensor"]

document_models = [
    User,
    Project,
    AshaDevice,
    Sensor
]
