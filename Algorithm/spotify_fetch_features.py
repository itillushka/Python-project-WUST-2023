"""
This module provides a function for fetching audio features for tracks using the Spotify API.
"""


def fetch_audio_features(sp, track_ids):
    """
        Fetches audio features for the tracks with the given ids.

        Args:
            sp (spotipy.Spotify): The Spotify client.
            track_ids (list): A list of track ids.

        Returns:
            list: A list of dictionaries containing audio features for the tracks.
    """
    features = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i + 100]
        audio_features = sp.audio_features(batch)
        for track in audio_features:
            if track is None:
                features.append({'danceability': 0, 'energy': 0, 'key': 0, 'loudness': 0, 'mode': 0, 'speechiness': 0,
                                 'acousticness': 0, 'instrumentalness': 0, 'liveness': 0, 'valence': 0, 'tempo': 0,
                                 'type': 'audio_features', 'id': '00000', 'uri': 'spotify:track:0',
                                 'track_href': 'https://api.spotify.com/', 'analysis_url': 'https://api.spotify.com/',
                                 'duration_ms': 0, 'time_signature': 0})
            else:
                features.append(track)
    return features
