from dataclasses import dataclass
import pandas as pd
from pathlib import Path

from .loaders import load_tesla_preheat


@dataclass
class TimeSeriesDataset:
    """
    Generic time-series dataset used by the simulator.
    """
    time_s: pd.Series
    battery_temp_c: pd.Series
    power_kw: pd.Series

    def duration_s(self) -> float:
        return float(self.time_s.iloc[-1] - self.time_s.iloc[0])

    def mean_power_kw(self) -> float:
        return float(self.power_kw.mean())

    def temperature_rise_c(self) -> float:
        return float(self.battery_temp_c.iloc[-1] - self.battery_temp_c.iloc[0])


class TeslaPreheatDataset:
    """
    Tesla battery preheating experiment dataset.
    Wraps raw Excel logs into a clean time-series interface.
    """

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)
        self._data = None

    def load(self) -> TimeSeriesDataset:
        if self._data is None:
            df = load_tesla_preheat(self.filepath)

            # enforce monotonic time (critical for simulation stability)
            if not df["time_s"].is_monotonic_increasing:
                raise ValueError("Time column is not monotonic increasing")

            self._data = TimeSeriesDataset(
                time_s=df["time_s"],
                battery_temp_c=df["battery_temp_c"],
                power_kw=df["power_kw"],
            )

        return self._data
