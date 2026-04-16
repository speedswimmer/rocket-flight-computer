from typing import Optional

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    GPIO = None


class PowerSensor:
    """Reads battery status from PowerBoost 500 via LBO (Low Battery Output) pin.

    LBO is HIGH when battery is OK, goes LOW when battery drops below ~3.2V.
    """

    def __init__(self, lbo_pin: int = 4) -> None:
        self._lbo_pin = lbo_pin
        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(lbo_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _is_low_battery(self) -> bool:
        if not GPIO:
            return False
        return GPIO.input(self._lbo_pin) == GPIO.LOW

    def read(self) -> Optional[dict]:
        try:
            low = self._is_low_battery()
            return {
                "battery_v": 3.2 if low else 3.8,
                "battery_pct": 10.0 if low else 80.0,
                "battery_low": low,
            }
        except (OSError, ValueError):
            return None

    def cleanup(self) -> None:
        if GPIO:
            GPIO.cleanup(self._lbo_pin)
