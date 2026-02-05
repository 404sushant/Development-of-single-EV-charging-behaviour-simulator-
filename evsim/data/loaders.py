import pandas as pd
from pathlib import Path


def load_tesla_data(filepath: str | Path) -> pd.DataFrame:
    df = pd.read_excel(filepath, sheet_name="Data1")
    df.columns = [c.strip() for c in df.columns]

    power_col = next(
        c for c in df.columns
        if "system" in c.lower() and "watt" in c.lower()
    )

    time_raw = pd.to_numeric(df["Time"], errors="coerce")
    df = df.loc[time_raw.notna()].copy()

    time_s = time_raw.loc[time_raw.notna()]
    time_s = time_s - time_s.iloc[0]

    out = pd.DataFrame({
        "time_s": time_s.values,
        "power_kw": df[power_col].astype(float).values / 1000.0,
        "pre_heating": df.get("Pre-Heating", False).astype(bool)
    })

    return out.reset_index(drop=True)
