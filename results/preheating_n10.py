# results/preheating_n10.py
# -------------------------------------------------
# Frozen results for Tesla battery preheating at -10 °C
# Derived from 09122020 Tesla n10 Preheat.xlsx
# -------------------------------------------------

PREHEAT_N10 = {
    "ambient_temp_c": -10.0,

    # Measured quantities
    "heating_duration_s": 3949.5,
    "avg_heating_power_kw": 7.25,
    "peak_heating_power_kw": 11.45,
    "heating_energy_kwh": 7.95,

    # Assumed thermal parameter (literature-based)
    "thermal_capacity_kwh_per_c": 0.65,

    # Inferred quantity
    "delta_T_c": 12.24,
}
