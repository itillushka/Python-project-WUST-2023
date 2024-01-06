import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from scipy.sparse import csr_matrix, hstack

# Spotify API credentials
cid = '1f48b38396b34931a2d1bade6adfb73c'
secret = '75b2ccc4c50b464da4d9e702c22f5c91'
username = '3133z6gge5d752p4zsybwl6l2hoa'
scope = 'user-library-read playlist-modify-public playlist-read-private'
redirect_uri = 'http://localhost:8000'

# Create a SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope)
token_info = sp_oauth.get_cached_token()

# Get access token
if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    response = input('Paste the above link into your browser, then paste the redirect url here: ')
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

# Authenticated client
sp = spotipy.Spotify(auth=token_info['access_token'])

# Get playlist data
""" PASTE LINK TO SPOTIFY PLAYLIST HERE """
sourcePlaylistID = 'https://open.spotify.com/playlist/22L1DCJqEJBQElMCjRavjw'
sourcePlaylist = sp.user_playlist(username, sourcePlaylistID)
tracks = sourcePlaylist["tracks"]
songs = tracks["items"]

track_ids = []
track_names = []

for i in range(0, len(songs)):
    if songs[i]['track']['id'] != None:  # Removes the local tracks in your playlist if there is any
        track_ids.append(songs[i]['track']['id'])
        track_names.append(songs[i]['track']['name'])

# Fetch audio features for tracks in batches of 100
features = []
for i in range(0, len(track_ids), 100):
    batch = track_ids[i:i + 100]
    audio_features = sp.audio_features(batch)
    for track in audio_features:
        if track is None:
            print(track)
            features.append({'danceability': 0, 'energy': 0, 'key': 0, 'loudness': 0, 'mode': 0, 'speechiness': 0,
                             'acousticness': 0, 'instrumentalness': 0, 'liveness': 0, 'valence': 0, 'tempo': 0,
                             'type': 'audio_features', 'id': '00000', 'uri': 'spotify:track:0',
                             'track_href': 'https://api.spotify.com/', 'analysis_url': 'https://api.spotify.com/',
                             'duration_ms': 0, 'time_signature': 0})
        else:
            features.append(track)

playlist_df = pd.DataFrame(features, index=track_names)
playlist_df = playlist_df[["id", "acousticness", "danceability", "duration_ms",
                           "energy", "instrumentalness", "key", "liveness",
                           "loudness", "mode", "speechiness", "tempo", "valence"]]
v = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 6), max_features=10000)
X_names_sparse = v.fit_transform(track_names)

random_ratings = np.random.randint(3, 11, size=len(playlist_df))

# Convert the array to a list
ratings_list = random_ratings.tolist()
print(ratings_list)

# Assign the list to the 'ratings' column of the DataFrame
playlist_df['ratings'] = ratings_list

X_train = playlist_df.drop(['id', 'ratings'], axis=1)
y_train = playlist_df['ratings']

X_scaled = StandardScaler().fit_transform(X_train)
pca = decomposition.PCA(n_components=8)
X_pca = pca.fit_transform(X_scaled)

X_train_last = csr_matrix(hstack([X_pca, X_names_sparse]))
min_members = min(playlist_df['ratings'].value_counts())
n_splits = max(2, min_members)
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

tree = DecisionTreeClassifier()
tree_params = {'max_depth': range(1, 11), 'max_features': range(4, 19)}
tree_grid = GridSearchCV(tree, tree_params, cv=skf, n_jobs=-1, verbose=True)
tree_grid.fit(X_train_last, playlist_df['ratings'])

rec_tracks = []
for i in playlist_df['id'].values.tolist():
    rec_tracks += sp.recommendations(seed_tracks=[i], limit=int(len(playlist_df) / 2))['tracks']

rec_track_ids = []
rec_track_names = []
for i in rec_tracks:
    rec_track_ids.append(i['id'])
    rec_track_names.append(i['name'])

# Fetch audio features for recommended tracks in batches of 100
rec_features = []
for i in range(0, len(rec_track_ids), 100):
    rec_batch = rec_track_ids[i:i + 100]
    rec_audio_features = sp.audio_features(rec_batch)
    for track in rec_audio_features:
        if track is None:
            rec_features.append({'danceability': 0, 'energy': 0, 'key': 0, 'loudness': 0, 'mode': 0, 'speechiness': 0,
                                 'acousticness': 0, 'instrumentalness': 0, 'liveness': 0, 'valence': 0, 'tempo': 0,
                                 'type': 'audio_features', 'id': '00000', 'uri': 'spotify:track:0',
                                 'track_href': 'https://api.spotify.com/', 'analysis_url': 'https://api.spotify.com/',
                                 'duration_ms': 0, 'time_signature': 0})
        else:
            rec_features.append(track)

rec_playlist_df = pd.DataFrame(rec_features, index=rec_track_ids)

X_test_names = v.transform(rec_track_names)

rec_playlist_df = rec_playlist_df[["acousticness", "danceability", "duration_ms",
                                   "energy", "instrumentalness", "key", "liveness",
                                   "loudness", "mode", "speechiness", "tempo", "valence"]]

tree_grid.best_estimator_.fit(X_train_last, y_train)
rec_playlist_df_scaled = StandardScaler().fit_transform(rec_playlist_df)
rec_playlist_df_pca = pca.transform(rec_playlist_df_scaled)
X_test_last = csr_matrix(hstack([rec_playlist_df_pca, X_test_names]))
y_pred_class = tree_grid.best_estimator_.predict(X_test_last)

rec_playlist_df['ratings'] = y_pred_class
rec_playlist_df = rec_playlist_df.sort_values('ratings', ascending=False)
rec_playlist_df = rec_playlist_df.reset_index()

recs_to_add = rec_playlist_df[rec_playlist_df['ratings'] >= 7]['index'].values.tolist()[:100]

# recs_to_add = rec_playlist_df[rec_playlist_df['ratings']==8]['index'].values.tolist()

playlist_recs = sp.user_playlist_create(username,
                                        name='Recommended Songs for Playlist by AI TestIllia - {}'.format(
                                            sourcePlaylist['name']))

for i in recs_to_add:
    sp.user_playlist_add_tracks(username, playlist_recs['id'], [i])

