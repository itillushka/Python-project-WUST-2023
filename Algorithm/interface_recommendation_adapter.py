import requests

from Algorithm.create_ratings import rate_songs
from Algorithm.predict_track_ratings import predict_track_ratings
from Algorithm.process_database import create_playlist_df, assign_ratings, create_rec_playlist_df, \
    assign_and_sort_ratings
from Algorithm.recommendation_algorithm import recommendation_algorithm
from Algorithm.spotify_collect_user_songs import collect_user_songs
from Algorithm.spotify_construct_playlist import construct_playlist
from Algorithm.spotify_fetch_features import fetch_audio_features
from Algorithm.time_converter import convert_ms_to_min_sec


def recommend_song(sp, sourcePlaylistID):
    """
       Recommends a song based on the given Spotify playlist.
       Args:
           sp (spotipy.Spotify): The Spotify client.
           sourcePlaylistID (str): The ID of the source playlist.
       Returns:
           tuple: A tuple containing the recommended playlist and track information.
       Raises:
           requests.exceptions.HTTPError: If an HTTP error occurs.
       """
    try:
        track_ids, track_names, sourcePlaylist = collect_user_songs(sp, sourcePlaylistID)

        # Fetch audio features for tracks
        features = fetch_audio_features(sp, track_ids)

        playlist_df = create_playlist_df(features, track_names)

        ratings_list = rate_songs(playlist_df)

        # Assign the list to the 'ratings' column of the DataFrame
        playlist_df['ratings'] = ratings_list
        playlist_df = assign_ratings(playlist_df, ratings_list)

        rec_track_ids, rec_track_names, v, tree_grid, X_train_last, y_train, pca = recommendation_algorithm(playlist_df,
                                                                                                            track_names,
                                                                                                            sp)

        # Fetch audio features for recommended tracks
        rec_features = fetch_audio_features(sp, rec_track_ids)

        X_test_names = v.transform(rec_track_names)

        rec_playlist_df = create_rec_playlist_df(rec_features, rec_track_ids)

        y_pred_class = predict_track_ratings(tree_grid, X_train_last, y_train, rec_playlist_df, pca, X_test_names)

        rec_playlist_df = assign_and_sort_ratings(rec_playlist_df, y_pred_class)
        playlist_recs, rec_ids = construct_playlist(rec_playlist_df, sp, sourcePlaylist)

        # Retrieve track details for each recommended track
        track_info = []
        for i in range(0, len(rec_ids), 50):
            response = sp.tracks(rec_ids[i:i + 50])
            #response.raise_for_status()  # Raise an HTTPError if the response was an error
            tracks = response['tracks']
            for track in tracks:
                duration_in_min_sec = convert_ms_to_min_sec(track['duration_ms'])
                track_info.append({
                    'title': track['name'],
                    'artist': track['artists'][0]['name'],
                    'duration': duration_in_min_sec
                })
        return playlist_recs, track_info
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 429:
            print("Too many requests, try after 24 hours")
        else:
            print(f"An HTTP error occurred: {err}")
