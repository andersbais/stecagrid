import aiohttp
from defusedxml import ElementTree as ET


class InverterAPI:
    def __init__(self, host, port, session):
        self._host = host
        self._port = port
        self._session = session

    async def validate_connection(self):
        try:
            response = await self._session.get(
                f"http://{self._host}:{self._port}/measurements.xml"
            )
            response.raise_for_status()
            data = await response.text()
            root = ET.fromstring(data)

            # Check for a specific key-value pair
            device = root.find("Device")
            if device is not None and "StecaGrid" in device.get("Name", ""):
                return device.get("Name", "")

            return False
        except aiohttp.ClientError:
            return False

    async def get_data(self):
        response = await self._session.get(
            f"http://{self._host}:{self._port}/measurements.xml"
        )
        response.raise_for_status()
        data = await response.text()
        root = ET.fromstring(data)

        measurements = {}
        for measurement in root.find("Device/Measurements"):
            type_ = measurement.get("Type")
            value = measurement.get("Value")
            unit = measurement.get("Unit")
            measurements[type_] = {"value": value, "unit": unit}

        return measurements
