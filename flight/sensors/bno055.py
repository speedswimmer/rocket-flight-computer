from typing import Optional


class BNO055Sensor:
    def __init__(self) -> None:
        import board
        import busio
        import adafruit_bno055
        i2c = busio.I2C(board.SCL, board.SDA)
        self._device = adafruit_bno055.BNO055_I2C(i2c)

    def read(self) -> Optional[dict]:
        try:
            euler = self._device.euler
            accel = self._device.linear_acceleration
            if euler is None or accel is None:
                return None
            return {
                "yaw": euler[0] or 0.0,
                "roll": euler[1] or 0.0,
                "pitch": euler[2] or 0.0,
                "accel_x": accel[0] or 0.0,
                "accel_y": accel[1] or 0.0,
                "accel_z": accel[2] or 0.0,
            }
        except (OSError, ValueError):
            return None
