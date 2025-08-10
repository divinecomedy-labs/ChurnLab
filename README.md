# ChurnLab


**ChurnLab** is a retention simulation testbed designed to model engagement dynamics in subscription-based user populations. It enables rigorous testing of recommendation strategies against a decay-based behavioral simulation environment, with realistic archetypes derived from empirical behavioral datasets.

This open-source project provides a modular and extensible foundation for simulating user churn, evaluating mitigation strategies, and benchmarking engagement models. ChurnLab is intended as a sandbox for research teams, data scientists, and SaaS developers aiming to explore user retention dynamics at scale.

---

## Key Features

- **Health-Based User Modeling**: Simulates user engagement and behavioral fatigue.
- **Realistic Archetypes**: User behavior archetypes are statistically derived and normalized, creating diverse challenge conditions.
- **Batch-Based Simulation**: Supports multi-day simulations with per-batch intervention tracking and longitudinal outcome analysis.
- **Baseline Strategy Agent**: A rule-based heuristic system serves as a reference point for retention strategy evaluation.
- **Energy Tracking System**: Assigns costs to interventions to simulate real-world infrastructure or operational expenditure models.
- **Dual Population Framework**: Designed to compare two systems (e.g., a baseline vs. a novel agent) under shared simulation conditions.
- **Modular Charting System**: Generates visual dashboards for churn, retention, energy use, and user archetype survival.

---

## Why ChurnLab?

Most retention testing is reactive and dependent on post-hoc analytics. ChurnLab offers a proactive approach: simulate, test, and validate strategies in a controlled environment before production deployment. By experimenting in a sandbox, practitioners can reduce experimentation costs, avoid user fatigue, and uncover optimal strategies for engagement sustainability.

---

## Getting Started

### Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies.

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-org/ChurnLab.git
    cd ChurnLab
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the simulation:
    ```bash
    python sim_engine.py
    ```

---

## Project Structure

```
ChurnLab/
│
├── sim_engine.py              # Entry point for the simulation run
├── runner.py                  # Core batch loop execution
├── config.py                  # Simulation constants and toggles
├── strategy/                  # Strategy modules and population agents
├── population/                # User generation and population logic
├── utils/                     # Archetypes and user behavior modeling
├── viz_tools.py               # Charting and dashboard generation
├── events/                    # Row generation for batches
└── output/                    # Stores generated dashboards and metrics
```

---

## Use Cases

- Evaluate a recommendation or retention strategy under realistic churn pressures.
- Create benchmark comparisons for academic or commercial modeling efforts.
- Visualize the tradeoffs between intervention intensity and business cost.
- Prototype early-stage SaaS behavior loops with minimal infrastructure.

---

## Contributing

This project is in active development. Contributions in the form of new baseline strategies, improved archetype sampling, or documentation are welcome. Please open an issue or submit a pull request with a clear description of your change.

---

## Custom Simulations

Organizations interested in adapting ChurnLab for private simulation stacks or extending the testbed to better reflect their unique user base are encouraged to get in touch. Advanced simulation design and system integration services are available. Each simulation is tailored to a specific business profile, and optimal performance requires bespoke configuration.

---

## License

**Polyform Noncommercial License 1.0.0**

Copyright 2025 Divine Comedy Labs LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to use,
copy, modify, and distribute the Software, for noncommercial purposes only,
subject to the following conditions:

1. Noncommercial Use Only. You may not use the Software for commercial purposes.
   A commercial purpose is one intended for commercial advantage or monetary compensation.

2. Attribution Required. Any use of this software must retain the original copyright
   notice and include a reference to the official ChurnLab repository:
   https://github.com/your-org/ChurnLab

3. Commercial Licensing. For commercial use, please contact:
   virgil@yourdomain.com

4. No Warranty. The software is provided “as is”, without warranty of any kind,
   express or implied, including but not limited to the warranties of merchantability,
   fitness for a particular purpose, and noninfringement.

See https://polyformproject.org/licenses/noncommercial/1.0.0/ for the full license text.

---

## Contact

To request simulation customization or business alignment discussions, please reach out via the project email provided in this repository.

# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
=======
Simulation lab for retention based systems, designed to pit two systems against each other and score users retained, ARR, and energy usage. 
>>>>>>> d6bc24d7eaaffc4cae1263127ffc48d694ec2093
