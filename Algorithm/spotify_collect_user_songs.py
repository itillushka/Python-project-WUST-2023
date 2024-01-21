"""
This module provides a function for collecting user songs from a Spotify playlist.
"""

from __init__ import username


def collect_user_songs(sp, sourcePlaylistID):
    """
        Collects user songs from the Spotify playlist with the given id.

        Args:
            sp (spotipy.Spotify): The Spotify client.
            sourcePlaylistID (str): The id of the source playlist.

        Returns:
            tuple: A tuple containing a list of track ids, a list of track names, and the source playlist data.
    """
    # Get playlist data
    sourcePlaylist = sp.user_playlist(username, sourcePlaylistID)
    tracks = sourcePlaylist["tracks"]
    songs = tracks["items"]

    track_ids = []
    track_names = []

    for i in range(0, len(songs)):
        if songs[i]['track']['id'] is not None:  # Removes the local tracks in your playlist if there is any
            track_ids.append(songs[i]['track']['id'])
            track_names.append(songs[i]['track']['name'])

    return track_ids, track_names, sourcePlaylist
