"""
This module provides functions for creating and processing playlist dataframes.
"""

import pandas as pd


def create_playlist_df(features, track_names):
    """
        Creates a dataframe for the playlist with the given features and track names.

        Args:
            features (list): A list of dictionaries containing track features.
            track_names (list): A list of track names.

        Returns:
            pd.DataFrame: A dataframe containing the playlist data.
    """
    playlist_df = pd.DataFrame(features, index=track_names)
    playlist_df = playlist_df[["id", "acousticness", "danceability", "duration_ms",
                               "energy", "instrumentalness", "key", "liveness",
                               "loudness", "mode", "speechiness", "tempo", "valence"]]
    return playlist_df


def assign_ratings(playlist_df, ratings_list):
    """
        Assigns ratings to the tracks in the playlist dataframe.

        Args:
            playlist_df (pd.DataFrame): The dataframe containing playlist data.
            ratings_list (list): A list of ratings for the tracks.

        Returns:
            pd.DataFrame: The dataframe with the assigned ratings.
    """
    playlist_df['ratings'] = ratings_list
    return playlist_df


def create_rec_playlist_df(rec_features, rec_track_ids):
    """
        Creates a dataframe for the recommended playlist with the given features and track ids.

        Args:
            rec_features (list): A list of dictionaries containing track features for the recommended tracks.
            rec_track_ids (list): A list of track ids for the recommended tracks.

        Returns:
            pd.DataFrame: A dataframe containing the recommended playlist data.
    """
    rec_playlist_df = pd.DataFrame(rec_features, index=rec_track_ids)
    rec_playlist_df = rec_playlist_df[["acousticness", "danceability", "duration_ms",
                                       "energy", "instrumentalness", "key", "liveness",
                                       "loudness", "mode", "speechiness", "tempo", "valence"]]
    return rec_playlist_df


def assign_and_sort_ratings(rec_playlist_df, y_pred_class):
    """
        Assigns and sorts ratings for the tracks in the recommended playlist dataframe.

        Args:
            rec_playlist_df (pd.DataFrame): The dataframe containing recommended playlist data.
            y_pred_class (list): A list of predicted ratings for the tracks.

        Returns:
            pd.DataFrame: The dataframe with the assigned and sorted ratings.
    """
    rec_playlist_df['ratings'] = y_pred_class
    rec_playlist_df = rec_playlist_df.sort_values('ratings', ascending=False)
    rec_playlist_df = rec_playlist_df.reset_index()
    return rec_playlist_df
