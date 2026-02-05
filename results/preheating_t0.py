# results/preheating_t0.py
# -------------------------------------------------
# Frozen results for Tesla battery preheating at 0 °C
# -------------------------------------------------

PREHEAT_T0 = {
    "ambient_temp_c": 0.0,

    # Verified from dataset:
    # No active preheating observed
    "heating_duration_s": 0.0,
    "avg_heating_power_kw": 0.0,
    "peak_heating_power_kw": 0.0,
    "heating_energy_kwh": 0.0,

    # Thermal parameter (assumed, not used here)
    "thermal_capacity_kwh_per_c": 0.65,

    # No temperature rise due to preheating
    "delta_T_c": 0.0,
}
