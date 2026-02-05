from evsim.models.soc import soc_update


def simulate_soc(time_s, power_kw, initial_soc, battery_capacity_kwh):
    soc = initial_soc
    soc_trace = [soc]

    for i in range(1, len(time_s)):
        dt = time_s[i] - time_s[i - 1]
        if dt <= 0:
            raise ValueError("Time must be strictly increasing")

        soc = soc_update(
            soc=soc,
            power_kw=power_kw[i],
            dt_s=dt,
            battery_capacity_kwh=battery_capacity_kwh
        )
        soc_trace.append(soc)

    return soc_trace
