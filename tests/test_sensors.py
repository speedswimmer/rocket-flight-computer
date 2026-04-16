import pytest
from unittest.mock import MagicMock, patch
from flight.sensors.bme280 import BME280Sensor
from flight.sensors.bno055 import BNO055Sensor
from flight.sensors.power import PowerSensor

class TestBME280:
    def test_read_returns_dict_with_required_keys(self):
        sensor = BME280Sensor.__new__(BME280Sensor)
        sensor._device = MagicMock()
        sensor._device.pressure = 1013.25
        sensor._device.temperature = 21.0
        sensor._device.relative_humidity = 45.0
        data = sensor.read()
        assert "pressure" in data
        assert "temperature" in data
        assert "humidity" in data
        assert data["pressure"] == pytest.approx(1013.25)

    def test_read_returns_none_on_error(self):
        sensor = BME280Sensor.__new__(BME280Sensor)
        sensor._device = MagicMock()
        type(sensor._device).pressure = property(
            lambda s: (_ for _ in ()).throw(OSError("I2C"))
        )
        data = sensor.read()
        assert data is None

class TestBNO055:
    def test_read_returns_orientation_and_accel(self):
        sensor = BNO055Sensor.__new__(BNO055Sensor)
        sensor._device = MagicMock()
        sensor._device.euler = (10.0, 20.0, 30.0)
        sensor._device.linear_acceleration = (0.1, 0.2, 9.8)
        data = sensor.read()
        assert data["yaw"] == pytest.approx(10.0)
        assert data["roll"] == pytest.approx(20.0)
        assert data["pitch"] == pytest.approx(30.0)
        assert data["accel_x"] == pytest.approx(0.1)

    def test_read_returns_none_on_error(self):
        sensor = BNO055Sensor.__new__(BNO055Sensor)
        sensor._device = MagicMock()
        type(sensor._device).euler = property(
            lambda s: (_ for _ in ()).throw(OSError("I2C"))
        )
        data = sensor.read()
        assert data is None

class TestPowerSensor:
    def test_read_returns_battery_info(self):
        sensor = PowerSensor.__new__(PowerSensor)
        sensor._read_voltage = MagicMock(return_value=3.9)
        data = sensor.read()
        assert "battery_v" in data
        assert "battery_pct" in data
        assert data["battery_v"] == pytest.approx(3.9)
        assert 0 <= data["battery_pct"] <= 100

    def test_voltage_to_percent_mapping(self):
        sensor = PowerSensor.__new__(PowerSensor)
        assert sensor._voltage_to_percent(4.2) == pytest.approx(100.0)
        assert sensor._voltage_to_percent(3.0) == pytest.approx(0.0)
        assert 0 < sensor._voltage_to_percent(3.7) < 100
