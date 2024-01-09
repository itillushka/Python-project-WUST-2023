"""
This module provides a function for predicting track ratings using a trained model.
"""

from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix, hstack


def predict_track_ratings(tree_grid, X_train_last, y_train, rec_playlist_df, pca, X_test_names):
    """
        Predicts track ratings using a trained model.

        Args:
            tree_grid (GridSearchCV): The trained model.
            X_train_last (csr_matrix): The training data.
            y_train (pd.Series): The training labels.
            rec_playlist_df (pd.DataFrame): The dataframe containing recommended playlist data.
            pca (PCA): The PCA object used for dimensionality reduction.
            X_test_names (list): A list of test track names.

        Returns:
            np.array: An array containing the predicted ratings.
    """
    tree_grid.best_estimator_.fit(X_train_last, y_train)
    rec_playlist_df_scaled = StandardScaler().fit_transform(rec_playlist_df)
    rec_playlist_df_pca = pca.transform(rec_playlist_df_scaled)
    X_test_last = csr_matrix(hstack([rec_playlist_df_pca, X_test_names]))
    y_pred_class = tree_grid.best_estimator_.predict(X_test_last)
    return y_pred_class