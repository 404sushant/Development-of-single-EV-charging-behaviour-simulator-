# scripts/example.py
# -------------------------------------------------
# Analysis script (not library code)
#
# Purpose:
# - Extract preheating power, duration, and energy
# - Attempt extraction of battery temperature rise ΔT
# - If unavailable, clearly report and allow inferred ΔT
# -------------------------------------------------

from evsim.data.loaders import load_tesla_data
from evsim.data.paths import TESLA_DATASETS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#  -------------------------------------------------
# PREHEATING POWER DATA
#  -------------------------------------------------

df = load_tesla_data(TESLA_DATASETS["n20_preheat"])
df = df.dropna().reset_index(drop=True)

heating_df = df[df["pre_heating"] == True]

heating_duration_s = (
    heating_df["time_s"].iloc[-1] - heating_df["time_s"].iloc[0]
)

avg_heating_power_kw = heating_df["power_kw"].mean()
peak_heating_power_kw = heating_df["power_kw"].max()

dt = heating_df["time_s"].diff().median()
heating_energy_kwh = (heating_df["power_kw"].sum() * dt) / 3600.0

#  -------------------------------------------------
# ATTEMPT BATTERY TEMPERATURE EXTRACTION (ΔT)
#  -------------------------------------------------

delta_T = None

try:
    bat_df = pd.read_excel(
        TESLA_DATASETS["n20_charging"],
        sheet_name="Data1"
    )
    bat_df.columns = [c.strip() for c in bat_df.columns]

    temp_candidates = [
        c for c in bat_df.columns
        if "batt" in c.lower() and "temp" in c.lower()
    ]

    if temp_candidates:
        battery_temp_col = temp_candidates[0]

        DATE = "2020-12-09"
        HEATER_ON  = "06:52"
        HEATER_OFF = "07:47"

        bat_df["timestamp"] = pd.to_datetime(
            DATE + " " + bat_df["Time"].astype(str),
            errors="coerce"
        )

        segment = bat_df[
            (bat_df["timestamp"] >= pd.Timestamp(f"{DATE} {HEATER_ON}")) &
            (bat_df["timestamp"] <= pd.Timestamp(f"{DATE} {HEATER_OFF}"))
        ].dropna(subset=[battery_temp_col])

        if not segment.empty:
            T_start = segment[battery_temp_col].iloc[0]
            T_end   = segment[battery_temp_col].iloc[-1]
            delta_T = T_end - T_start

except Exception as e:
    print("Battery temperature extraction failed:", e)

#  -------------------------------------------------
# PRINTING RESULTS
#  -------------------------------------------------

print(" PREHEATING (-20 °C) RESULTS ")
print(f"Heating duration [s]: {heating_duration_s:.1f}")
print(f"Average heating power [kW]: {avg_heating_power_kw:.2f}")
print(f"Peak heating power [kW]: {peak_heating_power_kw:.2f}")
print(f"Heating energy [kWh]: {heating_energy_kwh:.2f}")
print()

if delta_T is not None:
    print(f"Extracted battery ΔT [°C]: {delta_T:.2f}")
    print(f"Thermal capacity [kWh/°C]: {heating_energy_kwh / delta_T:.3f}")
else:
    print("Battery temperature not available in dataset.")
    print("ΔT must be inferred using calibrated thermal capacity.")

#  -------------------------------------------------
# SANITY PLOT
#  -------------------------------------------------

plt.figure()
plt.plot(df["time_s"], df["power_kw"])
plt.xlabel("Time [s]")
plt.ylabel("Power [kW]")
plt.title("Battery preheating power profile (-20 °C)")
plt.grid(True)
plt.show()


# -------------------------------------------------
# Battery temperature rise estimation (ΔT)
# -------------------------------------------------
# Method:
# Internal battery temperature measurements were not available in the dataset.
# Therefore, battery temperature rise is inferred using an energy balance
# approach based on a lumped thermal model:
#
#     E_heat = C_th * ΔT
#
# where:
#   E_heat = electrical energy consumed during preheating (measured)
#   C_th   = effective battery thermal capacity (assumed from literature)
#   ΔT     = inferred battery temperature rise
#
# Rearranged:
#     ΔT = E_heat / C_th
#
# Based on literature values for lithium-ion battery specific heat capacity
# and typical battery pack masses, an effective thermal capacity in the range
# 0.5–1.0 kWh/°C is commonly used in simplified thermal models.
# In this work, a nominal value of 0.65 kWh/°C is adopted.

# Measured heating energy [kWh]
E_heat_kwh = heating_energy_kwh

# Assumed effective thermal capacity [kWh/°C]
C_th_kwh_per_c = 0.65

# Inferred battery temperature rise [°C]
delta_T_c = E_heat_kwh / C_th_kwh_per_c

print("Heating energy [kWh]:", E_heat_kwh)
print("Assumed thermal capacity [kWh/°C]:", C_th_kwh_per_c)
print("Inferred battery temperature rise ΔT [°C]:", delta_T_c)

# -------------------------------------------------
# Sensitivity analysis (robustness check)
# -------------------------------------------------
# To assess the influence of the assumed thermal capacity, ΔT is also
# evaluated for a range of plausible C_th values reported in literature.

print("\nSensitivity analysis for thermal capacity:")
for C in [0.5, 0.65, 0.8]:
    print(
        f"C_th = {C:.2f} kWh/°C -> "
        f"ΔT = {E_heat_kwh / C:.2f} °C"
    )




from evsim.data.loaders import load_tesla_data
from evsim.data.paths import TESLA_DATASETS

df = load_tesla_data(TESLA_DATASETS["t0_preheat"])
df = df.dropna().reset_index(drop=True)

print("Unique values of Pre-Heating flag:")
print(df["pre_heating"].value_counts())

