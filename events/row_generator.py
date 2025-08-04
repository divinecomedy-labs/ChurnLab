import random
import numpy as np
import pandas as pd
from datetime import timedelta
from utils.constants import ARCHETYPES, EVENT_PROBS_BY_STATE, EVENT_TYPES, EVENT_TYPE_SCORES,  ROLLING_WINDOW
from numpy.random import default_rng
from config import rng




def simulate_absence_pressure(user_health: float) -> bool:
    """
    Determines whether a user appears in this batch based on their current health score.

    Health acts as a proxy for engagement readiness. Users in higher health states are
    more likely to generate events in a given batch. This simulates behavioral decay.
    """
    if user_health >= 0.8:
        return True  # Highly engaged users are always present
    elif user_health >= 0.5:
        return random.random() < 0.95  # Strong presence likelihood
    elif user_health >= 0.2:
        return random.random() < 0.8   # Moderately present
    else:
        return random.random() < 0.4  # Mostly absent
    
def generate_rows_for_user(uid, ts, user_info):
    """
        Generates a synthetic batch of engagement events for a single user.

        This function simulates real-world user variability through a mixture of:
        - Predefined archetypes (behavioral fingerprints)
        - Fatigue and cooldown dynamics
        - Health-based presence gating
        - Controlled volatility for row counts
        - Timed event density reflecting behavioral health
        - Customizable event types and severities
        """
    
    # Extract user attributes
    archetype = ARCHETYPES[user_info["archetype"]]
    state = user_info["state"]
    user_health = user_info["user_health"]
    fatigue = user_info["fatigue"]
    cooldown = user_info["cooldown"]
    activity = user_info["activity"]
    value_tier = user_info["value"]
    recovery = user_info["recovered"]

    # Archetype-specific baseline engagement behavior
    row_mean = archetype["row_mean"]
    volatility = archetype["volatility"]
    state_row_mult = archetype["state_row_mult"].get(state, 1.0)

    # Determine if user is present this batch based on health gating
    if not simulate_absence_pressure(user_health):
        return pd.DataFrame()

    # Engagement row generation: dynamic adjustment for fatigue, cooldown, activity, state
    fatigue_damp = max(0.0, 1 - fatigue)
    activity_factor = np.mean(activity)
    cooldown_factor = 1 - min(1.0, 1 / (cooldown + 1))
    base_count = row_mean * user_health * fatigue_damp * activity_factor * state_row_mult * cooldown_factor

    # Introduce controlled volatility into row count to reflect behavioral variance
    noisy_count = int(np.clip(np.random.normal(loc=base_count, scale=base_count * volatility), 0, None))
    if noisy_count == 0:
        return pd.DataFrame()

    # Timestamp generation: event distribution varies with health
    if user_health >= 0.8:
        timestamps = [ts + timedelta(minutes=i) for i in range(noisy_count)]
    elif user_health >= 0.5:
        timestamps = sorted([ts + timedelta(minutes=random.randint(0, 30)) for _ in range(noisy_count)])
    elif user_health >= 0.2:
        timestamps = sorted([ts + timedelta(minutes=random.randint(0, 60)) for _ in range(noisy_count)])
    else:
        timestamps = sorted([ts + timedelta(minutes=random.randint(0, 180)) for _ in range(noisy_count)])

    # Event type and severity sampling — tied to state and archetype distributions
    event_probs = EVENT_PROBS_BY_STATE.get(state, [0.2, 0.4, 0.3, 0.05, 0.05])
    event_types = rng.choice(EVENT_TYPES, p=event_probs, size=noisy_count)
    event_severity = rng.choice(["low", "medium", "high"], p=[0.4, 0.4, 0.2], size=noisy_count)
    engagement_scores = [EVENT_TYPE_SCORES.get(ev, 0) for ev in event_types]

    # Final structured output for downstream simulation processing
    return pd.DataFrame({
        "uid": [uid] * noisy_count,
        "timestamp": timestamps,
        "event_type": event_types,
        "event_severity": event_severity,
        "session_id": [f"{uid}_{ts.date()}" for _ in range(noisy_count)],
        "session_position": list(range(noisy_count)),
        "engagement_score": engagement_scores,
        "user_health": [user_health] * noisy_count,
        "fatigue": [fatigue] * noisy_count,
        "cooldown": [cooldown] * noisy_count,
        "value_tier": [value_tier] * noisy_count,
        "state": [state] * noisy_count,
        "rolling_activity": [activity_factor] * noisy_count,
        "recovered": [recovery] * noisy_count
    })

# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/