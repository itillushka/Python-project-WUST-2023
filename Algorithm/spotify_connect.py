"""
This module provides a function for connecting to the Spotify API.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Algorithm.config import cid, secret, redirect_uri, scope, hardcoded_token
import requests


# Create a SpotifyOAuth object
def connect_sp():
    """
        Connects to the Spotify API and returns a Spotify client.

        Returns:
            spotipy.Spotify: The Spotify client.
    """
    sp_oauth = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope)
    token_info = sp_oauth.get_cached_token()

    # Check if server is running
    try:
        response = requests.get(redirect_uri)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print("Something went wrong with the server.")
        return

    # Get access token
    if not token_info:
        try:
            # Try to use hardcoded token
            sp = spotipy.Spotify(auth=hardcoded_token)
            sp.current_user()  # This will raise an exception if the token is not valid
            print("Using hardcoded token.")
        except spotipy.exceptions.SpotifyException:
            # If hardcoded token is not valid, ask the user to paste the link
            auth_url = sp_oauth.get_authorize_url()
            print(f'Please go to the following URL: {auth_url}')
            response = input('Then paste the redirect url here: ')
            code = sp_oauth.parse_response_code(response)
            token_info = sp_oauth.get_access_token(code)
            sp = spotipy.Spotify(auth=token_info['access_token'])
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])

    return sp
