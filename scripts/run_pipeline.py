from evsim.data.paths import TESLA_DATASETS
from evsim.data.loaders import load_tesla_data
from evsim.simulator import simulate_soc

TEMPERATURE_OPTIONS = {
    "1": ("0 °C", "t0_drive"),
    "2": ("-10 °C", "n10_drive"),
    "3": ("-20 °C", "n20_drive"),
}


def main():
    print("\n=== EV SOC SIMULATOR ===")
    for k, (label, _) in TEMPERATURE_OPTIONS.items():
        print(f"{k} → {label}")

    choice = input("Select temperature: ").strip()
    if choice not in TEMPERATURE_OPTIONS:
        print("Invalid selection")
        return

    label, dataset_key = TEMPERATURE_OPTIONS[choice]
    print(f"\nRunning SOC simulation at {label}")

    df = load_tesla_data(TESLA_DATASETS[dataset_key])

    charging_df = df[
        (df["power_kw"] > 0) &
        (df["pre_heating"] == False)
    ]

    time_s = charging_df["time_s"].values
    power_kw = charging_df["power_kw"].values

    soc_trace = simulate_soc(
        time_s=time_s,
        power_kw=power_kw,
        initial_soc=0.20,
        battery_capacity_kwh=75.0
    )

    print(f"Initial SOC: 0.20")
    print(f"Final SOC:   {soc_trace[-1]:.3f}")
    print(f"Charging time [h]: {(time_s[-1] - time_s[0]) / 3600:.2f}")


if __name__ == "__main__":
    main()
