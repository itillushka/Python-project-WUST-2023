"""
This module provides a function for performing the recommendation algorithm on a given playlist.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from scipy.sparse import csr_matrix, hstack
from sklearn.model_selection import GridSearchCV


def recommendation_algorithm(playlist_df, track_names, sp):
    """
        Performs the recommendation algorithm on a given playlist.

        Args:
            playlist_df (pd.DataFrame): The dataframe containing playlist data.
            track_names (list): A list of track names.
            sp (spotipy.Spotify): The Spotify client.

        Returns:
            tuple: A tuple containing recommended track ids, track names, TfidfVectorizer object,
                GridSearchCV object, training data, training labels, and PCA object.
    """
    v = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 6), max_features=10000)
    X_names_sparse = v.fit_transform(track_names)

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

    return rec_track_ids, rec_track_names, v, tree_grid, X_train_last, y_train, pca
