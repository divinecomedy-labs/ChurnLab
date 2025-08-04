# === State Transition and Strategy Effects ===
# The RULES dictionary governs how each strategy affects a user depending on their current state.
# It defines the next state, health delta, and any incurred penalty for inappropriate actions.
# This behavioral map serves as the engine for engagement simulation dynamics.

RULES = {
    # --- Stable State ---
    ("stable", "observe"):   {"next": "stable",     "d_health": +0.01, "penalty": 0},
    ("stable", "monitor"):   {"next": "stable",     "d_health": +0.01, "penalty": 0},
    ("stable", "nudge"):     {"next": "stable",     "d_health": +0.01, "penalty": 0},
    ("stable", "reinforce"): {"next": "stable",     "d_health": +0.02, "penalty": 0},
    ("stable", "support"):   {"next": "cycling",    "d_health": -0.02, "penalty": 1},
    ("stable", "redirect"):  {"next": "erratic",    "d_health": -0.22, "penalty": 2},
    ("stable", "boost"):     {"next": "cycling",    "d_health": -0.03, "penalty": 2},
    ("stable", "escalate"):  {"next": "erratic",    "d_health": -0.13, "penalty": 3},
    ("stable", "suppress"):  {"next": "disrupted",  "d_health": -0.15, "penalty": 3},

    # --- Erratic State ---
    ("erratic", "observe"):   {"next": "erratic",    "d_health":  0.00, "penalty": 1},
    ("erratic", "monitor"):   {"next": "cycling",    "d_health": +0.02, "penalty": 0},
    ("erratic", "nudge"):     {"next": "cycling",    "d_health": +0.03, "penalty": 0},
    ("erratic", "reinforce"): {"next": "recovering", "d_health": +0.04, "penalty": 0},
    ("erratic", "support"):   {"next": "recovering", "d_health": +0.03, "penalty": 0},
    ("erratic", "redirect"):  {"next": "recovering", "d_health": +0.05, "penalty": 0},
    ("erratic", "boost"):     {"next": "recovering", "d_health": +0.02, "penalty": 1},
    ("erratic", "escalate"):  {"next": "disrupted",  "d_health": -0.22, "penalty": 2},
    ("erratic", "suppress"):  {"next": "disrupted",  "d_health": -0.14, "penalty": 2},

    # --- Cycling State ---
    ("cycling", "observe"):   {"next": "cycling",    "d_health":  0.00, "penalty": 1},
    ("cycling", "monitor"):   {"next": "cycling",    "d_health": +0.01, "penalty": 0},
    ("cycling", "nudge"):     {"next": "recovering", "d_health": +0.02, "penalty": 0},
    ("cycling", "reinforce"): {"next": "recovering", "d_health": +0.03, "penalty": 0},
    ("cycling", "support"):   {"next": "recovering", "d_health": +0.04, "penalty": 0},
    ("cycling", "redirect"):  {"next": "recovering", "d_health": +0.05, "penalty": 0},
    ("cycling", "boost"):     {"next": "erratic",    "d_health": -0.05, "penalty": 1},
    ("cycling", "escalate"):  {"next": "erratic",    "d_health": -0.15, "penalty": 2},
    ("cycling", "suppress"):  {"next": "disrupted",  "d_health": -0.12, "penalty": 2},

    # --- Recovering State ---
    ("recovering", "observe"):   {"next": "recovering", "d_health": +0.01, "penalty": 0},
    ("recovering", "monitor"):   {"next": "stable",     "d_health": +0.02, "penalty": 0},
    ("recovering", "nudge"):     {"next": "stable",     "d_health": +0.03, "penalty": 0},
    ("recovering", "reinforce"): {"next": "stable",     "d_health": +0.04, "penalty": 0},
    ("recovering", "support"):   {"next": "stable",     "d_health": +0.05, "penalty": 0},
    ("recovering", "redirect"):  {"next": "stable",     "d_health": +0.02, "penalty": 1},
    ("recovering", "boost"):     {"next": "erratic",    "d_health": -0.11, "penalty": 1},
    ("recovering", "escalate"):  {"next": "disrupted",  "d_health": -0.13, "penalty": 2},
    ("recovering", "suppress"):  {"next": "disrupted",  "d_health": -0.15, "penalty": 3},

    # --- Disrupted State ---
    ("disrupted", "observe"):   {"next": "erratic",    "d_health": +0.01, "penalty": 1},
    ("disrupted", "monitor"):   {"next": "recovering", "d_health": +0.02, "penalty": 0},
    ("disrupted", "nudge"):     {"next": "recovering", "d_health": +0.03, "penalty": 0},
    ("disrupted", "reinforce"): {"next": "recovering", "d_health": +0.04, "penalty": 0},
    ("disrupted", "support"):   {"next": "recovering", "d_health": +0.05, "penalty": 0},
    ("disrupted", "redirect"):  {"next": "cycling",    "d_health": +0.02, "penalty": 1},
    ("disrupted", "boost"):     {"next": "erratic",    "d_health": -0.04, "penalty": 2},
    ("disrupted", "escalate"):  {"next": "erratic",    "d_health": -0.15, "penalty": 2},
    ("disrupted", "suppress"):  {"next": "disrupted",  "d_health": -0.01, "penalty": 0},  # assumed neutral suppress
}


# === Archetype Definitions ===
# Archetypes represent user personas with distinct behavioral tendencies.
# These drive stochastic simulation diversity and ground the system in realistic variance.


ARCHETYPES = {
 'Steady Performer': {
     'user_health_mult': 1.02,
     'fatigue_mult': 0.07,
     'row_mean': 9,
     'volatility': 0.07,
     'cooldown': 8,
     'state_row_mult': {
         'stable': 1.0,
         'cycling': 0.9,
         'erratic': 0.75,
         'recovering': 0.85,
         'disrupted': 0.3
     }
 },
 'At-Risk Minimalist': {
     'user_health_mult': 0.61,
     'fatigue_mult': 0.10,
     'row_mean': 8,
     'volatility': 0.10,
     'cooldown': 8,
     'state_row_mult': {
         'stable': 1.0,
         'cycling': 0.9,
         'erratic': 0.75,
         'recovering': 0.85,
         'disrupted': 0.3
     }
 },
 'Quiet Churner': {
     'user_health_mult': 0.78,
     'fatigue_mult': 0.09,
     'row_mean': 6,
     'volatility': 0.09,
     'cooldown': 9,
     'state_row_mult': {
         'stable': 1.0,
         'cycling': 0.9,
         'erratic': 0.75,
         'recovering': 0.85,
         'disrupted': 0.3
     }
 },
 'Erratic Veteran': {
     'user_health_mult': 0.62,
     'fatigue_mult': 0.10,
     'row_mean': 9,
     'volatility': 0.10,
     'cooldown': 8,
     'state_row_mult': {
         'stable': 1.0,
         'cycling': 0.9,
         'erratic': 0.75,
         'recovering': 0.85,
         'disrupted': 0.3
     }
 },
 'Inconsistent Contributor': {
     'user_health_mult': 0.65,
     'fatigue_mult': 0.10,
     'row_mean': 7,
     'volatility': 0.10,
     'cooldown': 9,
     'state_row_mult': {
         'stable': 1.0,
         'cycling': 0.9,
         'erratic': 0.75,
         'recovering': 0.85,
         'disrupted': 0.3
     }
 },
 'Engaged Opportunist': {
     'user_health_mult': 0.75,
     'fatigue_mult': 0.09,
     'row_mean': 9,
     'volatility': 0.09,
     'cooldown': 8,
     'state_row_mult': {
         'stable': 1.0,
         'cycling': 0.9,
         'erratic': 0.75,
         'recovering': 0.85,
         'disrupted': 0.3
     }
 },
 'Stable High Value': {
     'user_health_mult': 1.05,
     'fatigue_mult': 0.07,
     'row_mean': 8,
     'volatility': 0.07,
     'cooldown': 8,
     'state_row_mult': {
         'stable': 1.0,
         'cycling': 0.9,
         'erratic': 0.75,
         'recovering': 0.85,
         'disrupted': 0.3
     }
 },
 'Recoverable Dropoff': {
     'user_health_mult': 1.00,
     'fatigue_mult': 0.08,
     'row_mean': 7,
     'volatility': 0.08,
     'cooldown': 9,
     'state_row_mult': {
         'stable': 1.0,
         'cycling': 0.9,
         'erratic': 0.75,
         'recovering': 0.85,
         'disrupted': 0.3
     }
 }
}
# === Event Simulation Parameters ===
# Defines the types of user behavior events and how they vary by state.
EVENT_TYPES = ["login", "browse", "interact", "purchase", "idle"]
EVENT_PROBS_BY_STATE = {
        "stable":     [0.2, 0.4, 0.3, 0.05, 0.05],
        "cycling":    [0.1, 0.3, 0.4, 0.1,  0.1],
        "erratic":    [0.05, 0.25, 0.4, 0.1, 0.2],
        "recovering": [0.3, 0.3, 0.2, 0.1,  0.1],
        "disrupted":  [0.1, 0.2, 0.3, 0.05, 0.35]
    }


# Scoring system to simulate implicit behavioral signals (can be extended).
EVENT_TYPE_SCORES = {
    "click": 1,
    "scroll": 0.5,
    "video_play": 2,
    "purchase": 5,
    "bounce": -1
}
# === Strategy Costs ===
# Maps each strategy to its simulated energy/infrastructure cost.
# This allows the simulation to model trade-offs between intervention intensity and efficiency.
STRATEGY_COSTS = {
    "observe":     0.01,  
    "monitor":     0.02,  
    "nudge":       0.02,
    "reinforce":   0.05,  
    "support":     0.05,
    "redirect":    0.05,
    "boost":       0.15,  
    "escalate":    0.15,
    "suppress":    0.10   
}


# === Tiered User Value Segments ===
# User segments are associated with different revenue potential (ARR) distributions.
# This anchors retention simulation to economic consequence.
VALUE_TIERS = ["basic", "pro", "enterprise"]
TIER_PROBS = [0.6, 0.3, 0.1]
TIER_ARR = {"basic": 120, "pro": 720, "enterprise": 6000}

# === Core Simulation Constants ===
STATES = ["stable","erratic","disrupted","recovering","cycling"]
STRATEGIES = ["observe", "monitor", "nudge", "reinforce", "support", "redirect", "boost", "escalate", "suppress"]
MAX_ROWS_PER_USER = 30                  # Hard cap for per-batch event row generation
FLAT_USER_HEALTH_DECAY = 0.005          # Global decay pressure on user engagement
ROLLING_WINDOW = 30                     # Batch window for smoothing engagement measures


# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/