from pathlib import Path

DATA_ROOT = Path("Tesla")

TESLA_DATASETS = {
    # 0 °C
    "t0_preheat": DATA_ROOT / "08122020 Tesla 0 Preheat.xlsx",
    "t0_drive": DATA_ROOT / "08122020 Tesla 0.xlsx",
    "t0_standby_night": DATA_ROOT / "07122020 Tesla 0 standby(night).xlsx",

    # −10 °C
    "n10_preheat": DATA_ROOT / "09122020 Tesla n10 Preheat.xlsx",
    "n10_drive": DATA_ROOT / "09122020 Tesla n10.xlsx",
    "n10_standby_night": DATA_ROOT / "08122020 Tesla n10 Standby(night).xlsx",

    # −20 °C
    "n20_preheat": DATA_ROOT / "10122020 Tesla n20 Preheat.xlsx",
    "n20_drive": DATA_ROOT / "10122020 Tesla n20.xlsx",
    "n20_standby_night": DATA_ROOT / "09122020 Tesla n20 Standby(night).xlsx",
}
