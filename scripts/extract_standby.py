# scripts/extract_standby.py
# -------------------------------------------------
# Standby (night) energy extraction script
# Purpose:
# - Quantify baseline energy consumption while parked
# - Capture cold-soak thermal protection behavior
# -------------------------------------------------

from evsim.data.loaders import load_tesla_data
from evsim.data.paths import TESLA_DATASETS


STANDBY_OPTIONS = {
    "1": ("0 °C", "t0_standby_night"),
    "2": ("-10 °C", "n10_standby_night"),
    "3": ("-20 °C", "n20_standby_night"),
}


def run_standby_extraction(dataset_key):
    # -------------------------------------------------
    # Load dataset
    # -------------------------------------------------
    df = load_tesla_data(TESLA_DATASETS[dataset_key])
    df = df.dropna().reset_index(drop=True)

    # -------------------------------------------------
    # Standby definition (IMPORTANT):
    # - Not charging (power < 0.5 kW)
    # - Not explicit pre-heating
    # This captures background + cold-soak protection
    # -------------------------------------------------
    standby_df = df[
        (df["pre_heating"] == False) &
        (df["power_kw"] < 0.5)
    ]

    print(f"\n=== Standby results for {dataset_key} ===")

    if standby_df.empty:
        print("No standby period detected.")
        print("Standby duration [s]: 0.0")
        print("Avg standby power [kW]: 0.0")
        print("Peak standby power [kW]: 0.0")
        print("Standby energy [kWh]: 0.0")
        print("Standby energy per hour [kWh/h]: 0.0")
        print("Equivalent 24h standby energy [kWh]: 0.0")
        return

    # -------------------------------------------------
    # Standby metrics
    # -------------------------------------------------
    standby_duration_s = (
        standby_df["time_s"].iloc[-1] - standby_df["time_s"].iloc[0]
    )

    avg_power_kw = standby_df["power_kw"].mean()
    peak_power_kw = standby_df["power_kw"].max()

    dt = standby_df["time_s"].diff().median()
    standby_energy_kwh = (standby_df["power_kw"].sum() * dt) / 3600.0

    # -------------------------------------------------
    # Derived interpretability metrics
    # -------------------------------------------------
    duration_h = standby_duration_s / 3600.0
    energy_per_hour_kwh = standby_energy_kwh / duration_h
    energy_24h_kwh = energy_per_hour_kwh * 24.0

    # -------------------------------------------------
    # Output
    # -------------------------------------------------
    print("Standby duration [s]:", round(standby_duration_s, 1))
    print("Avg standby power [kW]:", round(avg_power_kw, 3))
    print("Peak standby power [kW]:", round(peak_power_kw, 3))
    print("Standby energy [kWh]:", round(standby_energy_kwh, 3))
    print("Standby energy per hour [kWh/h]:", round(energy_per_hour_kwh, 3))
    print("Equivalent 24h standby energy [kWh]:", round(energy_24h_kwh, 3))


if __name__ == "__main__":
    while True:
        print("\nSelect standby dataset:")
        for k, (label, _) in STANDBY_OPTIONS.items():
            print(f"  {k} → {label}")
        print("  q → quit")

        choice = input("Enter selection: ").strip()

        if choice.lower() == "q":
            print("Exiting standby extractor.")
            break

        if choice not in STANDBY_OPTIONS:
            print("Invalid selection. Try again.")
            continue

        label, dataset_key = STANDBY_OPTIONS[choice]
        print(f"\nRunning standby extraction for {label}")
        run_standby_extraction(dataset_key)
