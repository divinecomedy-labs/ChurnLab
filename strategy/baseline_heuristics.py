import random

def compute_baseline_actions(batch_num, alive_users, user_health, value, fatigue, last_actions,
                             activity_window, cooldown=3, chaos_prob=0.03):
    """
    A simple heuristic policy engine designed to simulate a production-style intervention system.
    Intended to act as a baseline model for evaluating strategy selection performance.

    Parameters:
        batch_num (int): Current simulation batch number.
        alive_users (set): Set of active user IDs.
        user_health (dict): Proxy for user stability or retention risk (0.0–1.0).
        value (dict): Value tier of the user (e.g., basic, pro, enterprise).
        fatigue (dict): Map of users' strategy fatigue levels.
        last_actions (dict): Tracks when the last action was taken on a user.
        activity_window (dict): Rolling window of recent activity (presence).
        cooldown (int): Minimum batches between interventions unless cooldown is violated.
        chaos_prob (float): Probability of injecting randomness into the system.

    Returns:
        dict: Mapping of user_id → selected strategy (string).
    """
    actions = {}

    for uid in alive_users:
        # Check cooldown; allow rare violations to simulate operational inconsistency
        last = last_actions.get(uid, -cooldown)
        cooldown_lapsed = random.random() < 0.1  # 10% chance to ignore cooldown
        if not cooldown_lapsed and (batch_num - last) < cooldown:
            actions[uid] = "delay"
            continue

        # Retrieve key user states
        bh = user_health[uid]            # Behavioral stability
        f = fatigue.get(uid, 0)          # Strategic fatigue
        tier = value.get(uid, "basic")   # Value tier (impacts aggressiveness)
        recent_activity = activity_window.get(uid, [1]*6)

        # Track presence acceleration/deceleration as a naive momentum signal
        trend_recent = sum(recent_activity[-3:])
        trend_past = sum(recent_activity[-6:-3])
        activity_trend = trend_recent - trend_past

        # --- Core Heuristic Rules with Known Imperfections ---
        # Fatigued users have reduced chance of being targeted
        if f >= 4:
            if random.random() < 0.15:
                action = "boost" if tier in ["pro", "enterprise"] else "reinforce"
            else:
                action = "suppress"
        # High health users typically left alone, unless slightly fatigued
        elif bh >= 0.85:
            if f < 3:
                action = "observe"
            else:
                action = "delay" if random.random() > 0.1 else "boost"
        # Moderate health users nudged or reinforced based on trend
        elif 0.5 <= bh < 0.85:
            if activity_trend >= 0:
                action = "reinforce"
            else:
                action = "boost" if tier in ["premium", "pro", "enterprise"] else "reinforce"
        # Low health users triaged differently based on tier and fatigue
        else:
            if tier == "enterprise":
                action = "escalate" if f < 3 else "delay"
            else:
                action = "boost" if f < 4 else "observe"

        # --- Chaos Factor ---
        # Rare stochastic override to mimic real-world operational noise
        if random.random() < chaos_prob:
            action = random.choice(["observe", "boost", "reinforce", "delay", "suppress", "escalate"])

        actions[uid] = action
        last_actions[uid] = batch_num  # Update action history

    return actions


# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/