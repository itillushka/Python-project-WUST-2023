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
            tuple: A tuple containing recommended track ids, track_names, TfidfVectorizer object,
                GridSearchCV object, training data, training labels, and PCA object.
    """
    # Initialize a TfidfVectorizer object with specific parameters
    # This will be used to convert the track names into a matrix of TF-IDF features
    v = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 6), max_features=10000)

    # Fit the vectorizer to the track names and transform the track names into a matrix of TF-IDF features
    X_names_sparse = v.fit_transform(track_names)

    # Prepare the training data and labels
    # The training data is all columns in the playlist dataframe except 'id' and 'ratings'
    # The labels are the 'ratings' column in the playlist dataframe
    X_train = playlist_df.drop(['id', 'ratings'], axis=1)
    y_train = playlist_df['ratings']

    # Standardize the features by removing the mean and scaling to unit variance
    X_scaled = StandardScaler().fit_transform(X_train)

    # Initialize a PCA object with 8 components
    # This will be used to reduce the dimensionality of the scaled features
    pca = decomposition.PCA(n_components=8)

    # Fit the PCA to the scaled features and apply dimensionality reduction
    X_pca = pca.fit_transform(X_scaled)

    # Combine the PCA-transformed features and the TF-IDF features into one matrix
    # This will be the final training data
    X_train_last = csr_matrix(hstack([X_pca, X_names_sparse]))

    # Determine the number of splits for StratifiedKFold
    # This is based on the minimum number of members in each class in the 'ratings' column
    min_members = min(playlist_df['ratings'].value_counts())
    n_splits = max(2, min_members)

    # Initialize a StratifiedKFold object with a specific number of splits
    # This will be used for cross-validation
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Initialize a DecisionTreeClassifier object
    # This will be used to classify the tracks based on their features
    tree = DecisionTreeClassifier()

    # Define the parameter grid for the decision tree
    tree_params = {'max_depth': range(1, 11), 'max_features': range(4, 19)}

    # Initialize a GridSearchCV object with the decision tree and its parameter grid
    # This will be used to find the best parameters for the decision tree
    tree_grid = GridSearchCV(tree, tree_params, cv=skf, n_jobs=-1, verbose=True)

    # Fit the GridSearchCV to the final training data and labels
    # This will train the decision tree with the best parameters found
    tree_grid.fit(X_train_last, playlist_df['ratings'])

    # Initialize an empty list to store the recommended tracks
    rec_tracks = []

    # For each track id in the playlist dataframe, get the recommended tracks from Spotify
    # The number of recommended tracks for each track id is half the number of tracks in the playlist
    for i in playlist_df['id'].values.tolist():
        rec_tracks += sp.recommendations(seed_tracks=[i], limit=int(len(playlist_df) / 2))['tracks']

    # Initialize empty lists to store the ids and names of the recommended tracks
    rec_track_ids = []
    rec_track_names = []

    # For each recommended track, append its id and name to the respective lists
    for i in rec_tracks:
        rec_track_ids.append(i['id'])
        rec_track_names.append(i['name'])

    # Return a tuple containing the recommended track ids, track names, TfidfVectorizer object,
    # GridSearchCV object, final training data, training labels, and PCA object
    return rec_track_ids, rec_track_names, v, tree_grid, X_train_last, y_train, pca