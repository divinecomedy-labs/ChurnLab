import numpy as np
from utils.constants import ARCHETYPES

def compute_user_influx_rate(user_states: dict) -> float:
    """
    Estimate the system-wide user influx rate based on overall user health.
    
    This function simulates a real-world user acquisition mechanism tied to 
    the current quality of user experience. Healthier ecosystems grow faster.
    
    Args:
        user_states (dict): Dictionary of current user state objects.
    
    Returns:
        float: Proportion of new users to introduce in the next batch.
    """
    if not user_states:
        return 0

    engagement_scores = []
    fatigue_scores = []

    for state in user_states.values():
        archetype = ARCHETYPES[state["archetype"]]
        activity_mean = np.mean(state["activity"])

        # Engagement is estimated from mean activity levels
        engagement_scores.append(activity_mean)

        # Fatigue is normalized by how sensitive this archetype is to fatigue
        fatigue_scores.append(state["fatigue"] / max(0.01, archetype["fatigue_mult"]))

    mean_engagement = np.mean(engagement_scores)
    mean_fatigue = np.mean(fatigue_scores)

    # Health is a weighted blend of engagement and inverse fatigue
    # Tuned to produce values between 0.0 (unhealthy) and 1.0 (healthy)
    health = np.clip((mean_engagement * 1.25) - (mean_fatigue * 0.75), 0.0, 1.0)

    # Base influx rate, modulated by system health
    base_growth_rate = 0.002  # Approximately 0.2% new users per batch
    
    # Growth slows as total population approaches capacity (10k cap modeled here)
    size_penalty = np.clip(len(user_states) / 10000, 0.0, 1.0)

     # Final influx rate accounts for both system health and size saturation
    influx_rate = base_growth_rate * health * (1.0 - size_penalty)
    return influx_rate


# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/