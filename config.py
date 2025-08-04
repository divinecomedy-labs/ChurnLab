import numpy as np
from collections import Counter

# ------------------------------------------------------------------------------
# CONFIGURATION MODULE — ChurnLab OSS Simulation Parameters
# ------------------------------------------------------------------------------

"""
Disclaimer:
This simulation is a pessimistic benchmark derived from patterns in the Netflix Prize dataset.
It does not reflect your specific user footprint and excludes proprietary modeling layers used in real-world deployments.

ChurnLab is designed to stress-test retention strategies under aggressive behavioral decay assumptions.
For tailored simulations that uncover deeper behavioral leverage points, contact our lab.

Note:
ChurnLab includes user activity events such as views, clicks, and shares.
These events are useful signals for event-aware retention strategies.
"""

# ------------------------------------------------------------------------------
# RANDOMNESS & SEED CONTROL
# ------------------------------------------------------------------------------

# Global random number generator for reproducible results
rng = np.random.default_rng(57)
# ------------------------------------------------------------------------------
# SIMULATION SCALE AND TIME CONFIG
# ------------------------------------------------------------------------------
NUM_USERS = 500         # Initial number of users at simulation start
MAX_USERS = 1000        # Max users allowed (controls influx ceiling)
BATCHES_PER_DAY = 6     # Number of engagement windows per day
DAYS = 365              # Total simulation span in days
TOTAL_BATCHES = DAYS * BATCHES_PER_DAY  # Total time steps in the simulation

# ------------------------------------------------------------------------------
# USER CHURNING PARAMETERS

# ------------------------------------------------------------------------------
CHURN_THRESHOLD = 0.9   # Health level below which users are removed from the population
                        # Try 0.002–0.004 for aggressive modeling (tunable)
# ------------------------------------------------------------------------------


# STRATEGY BUDGET & FATIGUE SYSTEM
# ------------------------------------------------------------------------------
FATIGUE_RECOVERY = 0.35      # Rate at which user fatigue recovers over time
MAX_FATIGUE = 5              # Maximum fatigue level before user becomes unresponsive
# ------------------------------------------------------------------------------
# Additional parameters are defined elsewhere in component modules
# ------------------------------------------------------------------------------


# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/