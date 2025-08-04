import sys
import os

class Challenger:
    """
    Challenger is a placeholder class for users to implement their own 
    strategy engine or decision-making model. 

    This class is automatically invoked during each simulation batch,
    and should contain logic that selects an appropriate action for each user
    based on their engagement profile and historical behavior.

    Example use case:
        - A simple rule-based agent using thresholds on user health
        - A lightweight bandit model trained on batch feedback
        - A transformer-based recommender system with embedded user state
    """

    def __init__(self):
        # Users should implement their initialization logic here,
        # such as loading model parameters or preparing memory buffers.
        pass

    def run(self, df, uid_col=None, time_col=None):
        """
        This function is called at every batch step of the simulation.
        It should return a dataframe with columns [uid, action],
        where each user ID is mapped to a chosen action string.

        Parameters:
            df (pd.DataFrame): The batch of user events.
            uid_col (str): The column name identifying user IDs.
            time_col (str): The column name for timestamped events.

        Returns:
            pd.DataFrame: A dataframe containing two columns: uid and action.

        Example return:
            pd.DataFrame({
                "uid": [101, 102, 103],
                "action": ["observe", "boost", "suppress"]
            })
        """
        raise NotImplementedError("Please implement your challenger model's `run()` method.")


# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/
