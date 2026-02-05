# scripts/extract_charging.py
# -------------------------------------------------
# Charging power extraction script
# Interactive version: 0, -10, -20 °C
# -------------------------------------------------

from evsim.data.loaders import load_tesla_data
from evsim.data.paths import TESLA_DATASETS


CHARGING_OPTIONS = {
    "1": ("0 °C", "t0_drive"),
    "2": ("-10 °C", "n10_drive"),
    "3": ("-20 °C (drive)", "n20_drive"),
    "4": ("-20 °C (charging reference)", "n20_charging"),
}


def run_charging_extraction(dataset_key):
    # -------------------------------------------------
    # Load dataset
    # -------------------------------------------------
    df = load_tesla_data(TESLA_DATASETS[dataset_key])
    df = df.dropna().reset_index(drop=True)

    # -------------------------------------------------
    # Charging condition:
    # power > 0 AND not pre-heating
    # -------------------------------------------------
    charging_df = df[
        (df["power_kw"] > 0) & (df["pre_heating"] == False)
    ]

    print(f"\n=== Charging results for {dataset_key} ===")

    if charging_df.empty:
        print("No charging detected.")
        print("Charging duration [s]: 0.0")
        print("Avg charging power [kW]: 0.0")
        print("Peak charging power [kW]: 0.0")
        print("Charging energy [kWh]: 0.0")
        return

    charging_duration_s = (
        charging_df["time_s"].iloc[-1] - charging_df["time_s"].iloc[0]
    )

    avg_power_kw = charging_df["power_kw"].mean()
    peak_power_kw = charging_df["power_kw"].max()

    dt = charging_df["time_s"].diff().median()
    charging_energy_kwh = (charging_df["power_kw"].sum() * dt) / 3600.0

    print("Charging duration [s]:", round(charging_duration_s, 1))
    print("Avg charging power [kW]:", round(avg_power_kw, 2))
    print("Peak charging power [kW]:", round(peak_power_kw, 2))
    print("Charging energy [kWh]:", round(charging_energy_kwh, 2))


if __name__ == "__main__":
    while True:
        print("\nSelect charging dataset:")
        for k, (label, _) in CHARGING_OPTIONS.items():
            print(f"  {k} → {label}")
        print("  q → quit")

        choice = input("Enter selection: ").strip()

        if choice.lower() == "q":
            print("Exiting charging extractor.")
            break

        if choice not in CHARGING_OPTIONS:
            print("Invalid selection. Try again.")
            continue

        label, dataset_key = CHARGING_OPTIONS[choice]
        print(f"\nRunning charging extraction for {label}")
        run_charging_extraction(dataset_key)
# -------------------------------------------------