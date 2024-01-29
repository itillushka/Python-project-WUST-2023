"""
This module provides a function for constructing a Spotify playlist with recommended songs.
"""

from Algorithm.config import username


def construct_playlist(rec_playlist_df, sp, sourcePlaylist):
    """
        Constructs a Spotify playlist with the recommended songs.

        Args:
            rec_playlist_df (pd.DataFrame): The dataframe containing recommended playlist data.
            sp (spotipy.Spotify): The Spotify client.
            sourcePlaylist (dict): The source playlist data.

        Returns:
            str: The Spotify link to the constructed playlist.
            list: The list of track IDs added to the playlist.
    """
    recs_to_add = rec_playlist_df[rec_playlist_df['ratings'] >= 6]['index'].values.tolist()[:60]

    playlist_recs = sp.user_playlist_create(username,
                                            name='Recommended Songs for Playlist by AI - {}'.format(
                                                sourcePlaylist['name']))
    added_track_ids = []  # List to store the IDs of the added tracks
    songs = 0
    for i in recs_to_add:
        sp.user_playlist_add_tracks(username, playlist_recs['id'], [i])
        added_track_ids.append(i)  # Append the track ID to the list
        songs += 1

    # Print the URL of the created playlist
    print(f"Playlist constructed. It contains: {songs} songs You can access it at the following URL:")
    print(playlist_recs['external_urls']['spotify'])
    return playlist_recs['external_urls']['spotify'], added_track_ids  # Return the playlist link and the list of track IDs