# evsim/plots.py
# -------------------------------------------------
# Plotting utilities for SOC simulation results
# Thesis-oriented: simple, clear, reproducible
# -------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


RESULTS_FILE = Path("results/soc_traces.csv")
FIG_DIR = Path("results/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_soc_results():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError("SOC results CSV not found.")
    return pd.read_csv(RESULTS_FILE)


def plot_soc_vs_time():
    """
    Plot SOC vs time for all temperatures.
    """
    df = load_soc_results()

    plt.figure()
    for temp in df["temperature"].unique():
        sub = df[df["temperature"] == temp]
        plt.plot(
            sub["time_s"] / 3600.0,
            sub["soc"],
            label=temp
        )

    plt.xlabel("Time [h]")
    plt.ylabel("State of Charge (-)")
    plt.title("SOC evolution during charging")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "soc_vs_time.png", dpi=300)
    plt.close()


def plot_soc_vs_normalized_time():
    """
    Plot SOC vs normalized time (0–1) to compare curve shapes.
    """
    df = load_soc_results()

    plt.figure()
    for temp in df["temperature"].unique():
        sub = df[df["temperature"] == temp]
        t_norm = (
            sub["time_s"] - sub["time_s"].min()
        ) / (sub["time_s"].max() - sub["time_s"].min())

        plt.plot(
            t_norm,
            sub["soc"],
            label=temp
        )

    plt.xlabel("Normalized time (-)")
    plt.ylabel("State of Charge (-)")
    plt.title("SOC evolution (normalized time)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "soc_vs_normalized_time.png", dpi=300)
    plt.close()


def plot_charging_time_vs_temperature():
    """
    Plot total charging time vs ambient temperature.
    """
    df = load_soc_results()

    summary = (
        df.groupby("temperature")["time_s"]
        .max()
        .reset_index()
    )
    summary["time_h"] = summary["time_s"] / 3600.0

    plt.figure()
    plt.bar(summary["temperature"], summary["time_h"])
    plt.xlabel("Ambient temperature")
    plt.ylabel("Charging time [h]")
    plt.title("Charging time vs ambient temperature")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "charging_time_vs_temperature.png", dpi=300)
    plt.close()


def plot_soc_gain_vs_temperature():
    """
    Plot total SOC gain vs ambient temperature.
    """
    df = load_soc_results()

    soc_start = df.groupby("temperature")["soc"].first()
    soc_end = df.groupby("temperature")["soc"].last()
    delta_soc = (soc_end - soc_start).reset_index(name="delta_soc")

    plt.figure()
    plt.bar(delta_soc["temperature"], delta_soc["delta_soc"])
    plt.xlabel("Ambient temperature")
    plt.ylabel("SOC increase (-)")
    plt.title("SOC gain during charging")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "soc_gain_vs_temperature.png", dpi=300)
    plt.close()


def generate_all_plots():
    """
    Generate all thesis plots.
    """
    plot_soc_vs_time()
    plot_soc_vs_normalized_time()
    plot_charging_time_vs_temperature()
    plot_soc_gain_vs_temperature()
    print("All SOC plots generated and saved.")


if __name__ == "__main__":
    generate_all_plots()
