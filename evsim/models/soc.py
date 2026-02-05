def soc_update(soc, power_kw, dt_s, battery_capacity_kwh):
    delta_soc = (power_kw * dt_s) / (3600.0 * battery_capacity_kwh)
    return min(max(soc + delta_soc, 0.0), 1.0)
