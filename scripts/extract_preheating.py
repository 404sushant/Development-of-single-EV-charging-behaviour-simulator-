# scripts/extract_preheating.py
# -------------------------------------------------
# Generic preheating extraction script
# Works for -20, -10, and 0 °C cases
# -------------------------------------------------

from evsim.data.loaders import load_tesla_data
from evsim.data.paths import TESLA_DATASETS

# Literature-based thermal capacity
C_th_kwh_per_c = 0.65



from evsim.data.loaders import load_tesla_data
from evsim.data.paths import TESLA_DATASETS

C_th_kwh_per_c = 0.65

PREHEAT_OPTIONS = {
    "1": ("0 °C", "t0_preheat"),
    "2": ("-10 °C", "n10_preheat"),
    "3": ("-20 °C", "n20_preheat"),
}


def run_preheating_extraction(dataset_key):
    df = load_tesla_data(TESLA_DATASETS[dataset_key])
    df = df.dropna().reset_index(drop=True)

    heating_df = df[df["pre_heating"] == True]

    print(f"\n=== Preheating results for {dataset_key} ===")

    if heating_df.empty:
        print("No active preheating detected.")
        print("Heating duration [s]: 0.0")
        print("Avg power [kW]: 0.0")
        print("Peak power [kW]: 0.0")
        print("Heating energy [kWh]: 0.0")
        print("Inferred ΔT [°C]: 0.0")
        return

    heating_duration_s = (
        heating_df["time_s"].iloc[-1] - heating_df["time_s"].iloc[0]
    )

    avg_power = heating_df["power_kw"].mean()
    peak_power = heating_df["power_kw"].max()

    dt = heating_df["time_s"].diff().median()
    energy_kwh = (heating_df["power_kw"].sum() * dt) / 3600.0

    delta_T = energy_kwh / C_th_kwh_per_c

    print("Heating duration [s]:", round(heating_duration_s, 1))
    print("Avg power [kW]:", round(avg_power, 2))
    print("Peak power [kW]:", round(peak_power, 2))
    print("Heating energy [kWh]:", round(energy_kwh, 2))
    print("Inferred ΔT [°C]:", round(delta_T, 2))


if __name__ == "__main__":
    while True:
        print("\nSelect preheating dataset:")
        for k, (label, _) in PREHEAT_OPTIONS.items():
            print(f"  {k} → {label}")
        print("  q → quit")

        choice = input("Enter selection: ").strip()

        if choice.lower() == "q":
            print("Exiting preheating extractor.")
            break

        if choice not in PREHEAT_OPTIONS:
            print("Invalid selection. Try again.")
            continue

        label, dataset_key = PREHEAT_OPTIONS[choice]
        print(f"\nRunning preheating extraction for {label}")
        run_preheating_extraction(dataset_key)
