from config import NUM_USERS
from population.user_generator import generate_single_user

class PopulationBranch:
    """
    Represents an isolated population in the simulation, either baseline or challenger.
    Each branch maintains its own user states, metrics, and model (if any).
    """

    def __init__(self, name, model=None):
        self.name = name
        self.model = model  # Optional injected strategy or model controlling this branch
        # Initialize a population of synthetic users
        self.user_states = {uid: generate_single_user(uid) for uid in range(NUM_USERS)}
        self.alive_users = set(self.user_states.keys())     # Track active user IDs
        self.churned_users = set()                          # Track users who have exited
        # Time-series tracking of key simulation metrics
        self.energy_usage = []         # kWh or cost per batch
        self.arr_retention = []        # Retained ARR over time
        self.last_actions = {}         # Last strategy applied per user
        self.penalty_history = []      # Policy penalty tracking (optional)
        self.comeback_history = []     # Tracks recovered users if logic allows

    def add_user(self, uid):
        """Add a new user to the population dynamically (e.g. influx)."""
        self.user_states[uid] = generate_single_user(uid)
        self.alive_users.add(uid)

    def remove_user(self, uid):
        """Mark a user as churned and remove them from active set."""
        self.churned_users.add(uid)
        self.alive_users.discard(uid)
        
    def user(self, uid):
        """Retrieve the full user state object for a given uid."""
        return self.user_states[uid]

    def is_alive(self, uid):
        """Check if a user is currently active."""
        return uid in self.alive_users

    def alive_uids(self):
        """Return a list of all currently active user IDs."""
        return list(self.alive_users)

    def update_metrics(self, energy, arr, penalties, comebacks):
        """
        Store key performance metrics for this batch:
        - energy (float): Energy or cost incurred
        - arr (float): ARR retained
        - penalties (int): Costly or penalized interventions
        - comebacks (int): Previously churned users reactivated
        """

        self.energy_usage.append(energy)
        self.arr_retention.append(arr)
        self.penalty_history.append(penalties)
        self.comeback_history.append(comebacks)
    

    

# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/