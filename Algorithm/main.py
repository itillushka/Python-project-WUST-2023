"""
This is the main module that orchestrates the execution of the music recommendation algorithm.
It collects user songs, fetches audio features, creates and rates playlists, predicts track ratings,
and constructs the final playlist.
"""

from spotify_construct_playlist import construct_playlist
import threading
from server import run
from spotify_connect import connect_sp
from spotify_collect_user_songs import collect_user_songs
from spotify_fetch_features import fetch_audio_features
from create_ratings import rate_songs
from process_database import create_playlist_df, assign_ratings, create_rec_playlist_df, assign_and_sort_ratings
from predict_track_ratings import predict_track_ratings
from recommendation_algorithm import recommendation_algorithm

# Start the server in a separate thread
server_thread = threading.Thread(target=run)
server_thread.start()

sp = connect_sp()

# PASTE LINK TO SPOTIFY PLAYLIST HERE
sourcePlaylistID = 'https://open.spotify.com/playlist/5Pw0s6ZYgE0GCAaEJ1XEI2?si=Cz9-N8l1TPiVSZ6esEhYdA&pi=e-xnBTT2VzSmOX'

track_ids, track_names, sourcePlaylist = collect_user_songs(sp, sourcePlaylistID)

# Fetch audio features for tracks
features = fetch_audio_features(sp, track_ids)

playlist_df = create_playlist_df(features, track_names)

ratings_list = rate_songs(playlist_df)

# Assign the list to the 'ratings' column of the DataFrame
playlist_df['ratings'] = ratings_list
playlist_df = assign_ratings(playlist_df, ratings_list)

rec_track_ids, rec_track_names, v, tree_grid, X_train_last, y_train, pca = recommendation_algorithm(playlist_df,
                                                                                                    track_names, sp)

# Fetch audio features for recommended tracks
rec_features = fetch_audio_features(sp, rec_track_ids)

X_test_names = v.transform(rec_track_names)

rec_playlist_df = create_rec_playlist_df(rec_features, rec_track_ids)

y_pred_class = predict_track_ratings(tree_grid, X_train_last, y_train, rec_playlist_df, pca, X_test_names)

rec_playlist_df = assign_and_sort_ratings(rec_playlist_df, y_pred_class)

construct_playlist(rec_playlist_df, sp, sourcePlaylist)
