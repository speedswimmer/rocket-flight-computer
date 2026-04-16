from typing import Optional


class PowerSensor:
    VOLTAGE_MIN = 3.0
    VOLTAGE_MAX = 4.2

    def __init__(self, adc_pin: int = 0) -> None:
        self._adc_pin = adc_pin
        try:
            import board
            import analogio
            self._adc = analogio.AnalogIn(board.A0)
        except (ImportError, RuntimeError):
            self._adc = None

    def _read_voltage(self) -> float:
        if self._adc is None:
            return 0.0
        raw = self._adc.value
        return (raw / 65535) * 3.3 * 2

    def _voltage_to_percent(self, voltage: float) -> float:
        pct = (voltage - self.VOLTAGE_MIN) / (self.VOLTAGE_MAX - self.VOLTAGE_MIN) * 100
        return max(0.0, min(100.0, pct))

    def read(self) -> Optional[dict]:
        try:
            voltage = self._read_voltage()
            return {
                "battery_v": round(voltage, 2),
                "battery_pct": round(self._voltage_to_percent(voltage), 1),
            }
        except (OSError, ValueError):
            return None
