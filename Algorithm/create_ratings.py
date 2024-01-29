"""
This module provides a function for generating random ratings for songs.
"""

import numpy as np


def rate_songs(playlist_df):
    """
        Generates random ratings for the songs in the playlist dataframe.

        Args:
            playlist_df (pd.DataFrame): The dataframe containing playlist data.

        Returns:
            list: A list of random ratings for the songs.
    """
    random_ratings = np.random.randint(3, 11, size=len(playlist_df))

    # Convert the array to a list
    ratings_list = random_ratings.tolist()
    print(ratings_list)
    return ratings_list
