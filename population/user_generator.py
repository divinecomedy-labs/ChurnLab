from datetime import timedelta
from collections import deque 
from config import NUM_USERS, rng
from utils.constants import ARCHETYPES, VALUE_TIERS, TIER_PROBS, ROLLING_WINDOW
from numpy.random import default_rng

# ------------------------------------------------------------------------------
# USER GENERATION MODULE
# ------------------------------------------------------------------------------
# This module provides two key functions:
# - `generate_single_user(uid)`: initializes one user instance with randomized traits.
# - `initialize_users()`: creates the full starting population for the simulation.
# Archetypes, value tiers, and fatigue modeling are derived from parameterized priors.
# ------------------------------------------------------------------------------

def generate_single_user(uid):
    """
    Initializes a single synthetic user profile with randomized attributes.

    Parameters:
    - uid (int): Unique identifier for the user.

    Returns:
    - dict: A dictionary representing the initialized state of the user.
    """
    archetype = rng.choice(list(ARCHETYPES.keys()))  # Assign user to a behavior template
    return {
        "state": "stable",  # Initial engagement state
        "user_health": rng.uniform(0.6, 1.0),  # Starting engagement vitality
        "fatigue": 0,  # Fatigue starts at 0 and accumulates over time
        "activity": deque([1]*ROLLING_WINDOW, maxlen=ROLLING_WINDOW),  # Track recent activity
        "value": rng.choice(VALUE_TIERS, p=TIER_PROBS),  # User's business impact tier
        "recovered": False,  # Flag for whether user has re-engaged after prior risk
        "archetype": archetype,  # Assigned behavioral type
        "cooldown": ARCHETYPES[archetype]['cooldown']  # Archetype-specific cooldown timer
    }

def initialize_users():
    """
    Initializes the full user population with diverse archetypes and randomized attributes.

    Returns:
    - dict: Mapping of user IDs to their initialized state dictionaries.
    """
    user_states = {}

    for uid in range(NUM_USERS):
        archetype = rng.choice(list(ARCHETYPES.keys()))
        user_states[uid] = {
            "state": "stable",
            "user_health": rng.uniform(0.6, 1.0),
            "fatigue": 0,
            "activity": deque([1]*ROLLING_WINDOW, maxlen=ROLLING_WINDOW),
            "value": rng.choice(VALUE_TIERS, p=TIER_PROBS),
            "recovered": False,
            "archetype": archetype,
            "cooldown": ARCHETYPES[archetype]['cooldown']
        }

    return user_states

# ------------------------------------------------------------------------------

# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/------------
