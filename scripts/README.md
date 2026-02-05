# EVSIM – Electric Vehicle Charging Simulation Library

`evsim` is a modular Python library designed for simulating electric vehicle (EV) charging sessions. The package includes core data structures, analytical charging models, placeholders for empirical models, dataset handling utilities, and basic visualization tools.

The library is intended for academic research and prototyping, particularly for use in energy consumption studies, charging infrastructure analysis, and EV-grid interaction modeling.

## Features

- **Core Data Structures**: Foundational classes for EV and charging session representation
- **Charging Models**: Analytical models for simulating charging behavior
- **Dataset Utilities**: Tools for handling and processing EV charging data
- **Visualization**: Basic plotting and analysis capabilities

## Installation

Clone the repository and ensure the project root is on your Python path:

```bash
git clone <your-repo-url>
cd THESIS
pip install matplotlib
```

## Quick Start

```python
from evsim.core import ChargingSessionConfig
from evsim.simulator import simulate_session
from evsim.plot import plot_session

cfg = ChargingSessionConfig(
    initial_soc=0.20,
    target_soc=0.80,
    battery_capacity_kwh=60.0,
    max_power_kw=50.0,
)

steps = simulate_session(cfg)
plot_session(steps)
```

## Documentation

For detailed documentation and examples, see the [docs](./docs) directory.

## License

## Modeling Scope and Design Decisions

This project intentionally adopts a data-driven, system-level approach.

- Charging power is taken directly from experimentally measured time-series data.
- No explicit CC–CV or battery acceptance models are used in simulation.
- Temperature is treated as a static operating condition defining each scenario.
- State of Charge (SOC) is computed via an energy balance formulation.

Some theoretical and exploratory modules (e.g. CC–CV models, empirical curve fitting)
are included for reference but are not part of the thesis simulation pipeline.
