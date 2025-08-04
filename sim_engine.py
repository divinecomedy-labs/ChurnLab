import argparse
import sys
from types import SimpleNamespace

from config import *
from strategy.challenger import Challenger
from population.PopulationBranch import PopulationBranch
from runner import run_batch_loop
from config import rng


def parse_args():
    """
    Parses command-line arguments to configure the simulation runtime.
    These arguments override defaults from config.py where specified.
    """
    
    parser = argparse.ArgumentParser(description="Run ChurnLab Simulation Engine")

    parser.add_argument("--days", type=int, default=DAYS,
                        help="Total number of days to simulate (default: from config.py)")
    parser.add_argument("--enable-influx", action="store_true",
                        help="Enable new user influx over time")
    parser.add_argument("--disable-influx", action="store_false", dest="enable_influx",
                        help="Disable influx (default)")
    parser.set_defaults(enable_influx=False)

    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility (default: 42)")
    parser.add_argument("--num-users", type=int, default=NUM_USERS,
                        help="Initial number of users (default from config)")
    parser.add_argument("--max-users", type=int, default=MAX_USERS,
                        help="Maximum user cap during influx (default from config)")
    parser.add_argument("--batches-per-day", type=int, default=BATCHES_PER_DAY,
                        help="How many intervention windows per day (default from config)")

    return parser.parse_args()


def update_config_from_args(args):
    """
    Creates a runtime configuration by merging global defaults with CLI overrides.
    Also re-seeds the global RNG to ensure run-level determinism.
    """
    runtime_config = SimpleNamespace(**globals())

    runtime_config.DAYS = args.days
    runtime_config.NUM_USERS = args.num_users
    runtime_config.MAX_USERS = args.max_users
    runtime_config.BATCHES_PER_DAY = args.batches_per_day
    runtime_config.TOTAL_BATCHES = args.days * args.batches_per_day

    # Reinitialize shared RNG to preserve deterministic behavior across modules
    global rng
    from numpy.random import default_rng
    rng = default_rng(args.seed)

    return runtime_config


def run_sim():
    """
    Main entry point to ChurnLab’s simulation loop.
    Initializes both the baseline and challenger populations, applies configuration,
    and launches the batch-level simulation process.
    """
    args = parse_args()
    config = update_config_from_args(args)

    print(f"Launching ChurnLab simulation...")
    print(f"• Days: {config.DAYS}")
    print(f"• Batches per day: {config.BATCHES_PER_DAY}")
    print(f"• Influx enabled: {args.enable_influx}")
    print(f"• Seed: {args.seed}")
    print(f"• Initial Users: {config.NUM_USERS}")
    print(f"• Max Users: {config.MAX_USERS}")
    print(f"{'-'*40}")

     # Initialize both challenger and baseline branches for tracking
    challenger = PopulationBranch(name="challenger", model=Challenger())
    baseline = PopulationBranch(name="baseline")

    # Core loop: executes per-batch simulation behavior
    run_batch_loop(challenger, baseline, config=config, enable_influx=args.enable_influx)


if __name__ == "__main__":
    run_sim()


# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/