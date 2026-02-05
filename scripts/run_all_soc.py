import pandas as pd
from evsim.data.paths import TESLA_DATASETS
from evsim.data.loaders import load_tesla_data
from evsim.simulator import simulate_soc

SCENARIOS = {
    "0C": "t0_drive",
    "-10C": "n10_drive",
    "-20C": "n20_drive",
}

INITIAL_SOC = 0.20
BATTERY_CAPACITY_KWH = 75.0

all_results = []

for label, key in SCENARIOS.items():
    df = load_tesla_data(TESLA_DATASETS[key])
    charging_df = df[(df["power_kw"] > 0) & (~df["pre_heating"])]

    time_s = charging_df["time_s"].values
    power_kw = charging_df["power_kw"].values

    soc = simulate_soc(
        time_s=time_s,
        power_kw=power_kw,
        initial_soc=INITIAL_SOC,
        battery_capacity_kwh=BATTERY_CAPACITY_KWH,
    )

    for t, s in zip(time_s, soc):
        all_results.append({
            "temperature": label,
            "time_s": t,
            "soc": s,
        })

out = pd.DataFrame(all_results)
out.to_csv("results/soc_traces.csv", index=False)

print("SOC simulations completed and saved.")
