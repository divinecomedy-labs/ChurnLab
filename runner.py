from datetime import datetime, timedelta
import pandas as pd
import math
from tqdm import tqdm

from utils.constants import ARCHETYPES, RULES, STRATEGY_COSTS, TIER_ARR, FLAT_USER_HEALTH_DECAY, ROLLING_WINDOW
from config import rng
from strategy.baseline_heuristics import compute_baseline_actions
from strategy.challenger import Challenger
from events.row_generator import generate_rows_for_user
from population.influx import compute_user_influx_rate
from population.user_generator import generate_single_user
from viz.viz_tools import generate_summary_charts


def run_batch_loop(challenger, baseline, config, enable_influx=False):
    # Determine the duration of a simulation batch in minutes
    batch_duration_minutes = 24 * 60 // config.BATCHES_PER_DAY
    start_ts = datetime.now()

    # Tracking performance across the simulation horizon
    real_churn, base_churn = [], []
    real_energy, base_energy = [], []
    arr_retained_real, arr_retained_base = [], []
    penalty_tracker, comeback_tracker = [], []
    annotations = []

    # === Main Batch Loop ===
    for batch in tqdm(range(config.TOTAL_BATCHES)):
        ts = start_ts + timedelta(minutes=batch * batch_duration_minutes)
        batch_rows = []
        energy_real, energy_base = 0, 0
        arr_real, arr_base = 0, 0
        penalties, comebacks = 0, 0

        # --- Generate synthetic user behavior (Challenger) ---
        for uid in challenger.alive_uids():
            user = challenger.user(uid)
            row_df = generate_rows_for_user(uid, ts, user)
            if not row_df.empty:
                batch_rows.append(row_df)
            user["activity"].append(1 if not row_df.empty else 0)

        if batch_rows:
            user_df = pd.concat(batch_rows, ignore_index=True)
        else:
            user_df = pd.DataFrame()
        # If no user events occurred, skip this batch
        if user_df.empty or "uid" not in user_df.columns:
            continue

        # === Determine actions for both systems ===

        # --- Challenger strategy selection ---
        result = challenger.model.run(df=user_df, uid_col="uid", time_col="timestamp") # insert your model call here
        actions_challenger = {uid: val["strategy"] for uid, val in result.items()}

        # --- Baseline heuristic actions ---
        activity_window = {
            uid: list(challenger.user(uid)["activity"])[-ROLLING_WINDOW:]
            for uid in challenger.alive_uids()
        }

        actions_base = compute_baseline_actions(
            batch_num=batch,
            alive_users=challenger.alive_uids(),
            user_health={uid: challenger.user(uid)["user_health"] for uid in challenger.alive_uids()},
            value={uid: challenger.user(uid)["value"] for uid in challenger.alive_uids()},
            fatigue={uid: challenger.user(uid)["fatigue"] for uid in challenger.alive_uids()},
            last_actions=challenger.last_actions,
            activity_window=activity_window
        )

        # === Apply actions and update both populations ===
        for uid in list(challenger.alive_uids()):
            
            # --- Challenger user update ---
            user = challenger.user(uid)
            action = actions_challenger.get(uid, "observe")
            rule = RULES.get((user["state"], action), {"next": user["state"], "d_health": 0, "penalty": 0})
            archetype = ARCHETYPES[user["archetype"]]

            # Apply health change and penalty based on rulebook
            log_mod = math.log1p(1 - user["user_health"])
            user["user_health"] = max(0.0, user["user_health"] + rule["d_health"] * archetype["user_health_mult"] * log_mod)
            user["user_health"] = max(0.0, user["user_health"] - FLAT_USER_HEALTH_DECAY)
            user["fatigue"] = min(config.MAX_FATIGUE, user["fatigue"] + rule["penalty"] * archetype["fatigue_mult"])
            user["state"] = rule["next"]

            # Track comeback events
            if not user["recovered"] and user.get("prev_user_health", 1.0) < 0.4 and user["user_health"] > 0.6:
                comebacks += 1
                user["recovered"] = True
            user["prev_user_health"] = user["user_health"]

            if user["user_health"] < 0.01:
                challenger.remove_user(uid)
                continue

            # Track energy and ARR     
            energy_real += STRATEGY_COSTS.get(action, 0.0)
            arr_real += TIER_ARR[user["value"]]
            penalties += rule["penalty"]

            # --- Baseline user update ---
            user_b = baseline.user(uid)
            action_b = actions_base.get(uid, "observe")
            rule_b = RULES.get((user_b["state"], action_b), {"next": user_b["state"], "d_health": 0, "penalty": 0})
            arch_b = ARCHETYPES[user_b["archetype"]]

            log_mod_b = math.log1p(1 - user_b["user_health"])
            user_b["user_health"] = max(0.0, user_b["user_health"] + rule_b["d_health"] * arch_b["user_health_mult"] * log_mod_b)
            user_b["user_health"] = max(0.0, user_b["user_health"] - FLAT_USER_HEALTH_DECAY)
            user_b["fatigue"] = min(config.MAX_FATIGUE, user_b["fatigue"] + rule_b["penalty"] * arch_b["fatigue_mult"])
            user_b["state"] = rule_b["next"]

            penalties += rule_b["penalty"]

            if user_b["user_health"] < 0.01:
                baseline.remove_user(uid)
                continue

            energy_base += STRATEGY_COSTS.get(action, 0.0)
            if user_b["user_health"] >= 0.2:
                arr_base += TIER_ARR[user_b["value"]]

        # === Aggregate metrics for visualization ===
        real_churn.append(1 - len(challenger.alive_users) / config.NUM_USERS)
        base_churn.append(1 - len(baseline.alive_users) / config.NUM_USERS)
        real_energy.append(energy_real)
        base_energy.append(energy_base)
        arr_retained_real.append(arr_real)
        arr_retained_base.append(arr_base)
        penalty_tracker.append(penalties)
        comeback_tracker.append(comebacks)

        # === Optional user influx support ===
        if enable_influx and batch % config.BATCHES_PER_DAY == 0:
            influx_rate = compute_user_influx_rate(challenger.user_states)
            num_influx = int(influx_rate * len(challenger.user_states))
            for _ in range(num_influx):
                new_uid = max(challenger.user_states) + 1
                challenger.add_user(new_uid)
                baseline.user_states[new_uid] = generate_single_user(new_uid)
                baseline.alive_users.add(new_uid)

     # === Print diagnostic stats at end of sim ===
    print("Final Real Churn (Challenger):", real_churn[-10:])
    print("Final Baseline Churn:", base_churn[-10:])

    # === Generate pitch-ready visualization charts ===
    generate_summary_charts(
        real_energy=real_energy,
        base_energy=base_energy,
        arr_retained_real=arr_retained_real,
        arr_retained_base=arr_retained_base,
        real_churn=real_churn,
        base_churn=base_churn,
        penalty_tracker=penalty_tracker,
        churned_users=challenger.churned_users,
        user_states=challenger.user_states,
        save=True
    )



# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/