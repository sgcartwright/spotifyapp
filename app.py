import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, render_template
import time
import requests

app = Flask(__name__)

# Set your secret key here. Replace 'YOUR_SECRET_KEY' with a secure random string.
app.secret_key = 'YOUR_SECRET_KEY'

# Set the session cookie name
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

# Constants
TOKEN_INFO = "token_info"

# Define 'ids' and 'url_error' in the global scope
ids = []
url_error = False

# Spotify OAuth Configuration
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="9431127543be46348364af906f7b95ef", # Insert appropriate client id
        client_secret="d60a280850a0453d9021f0f4cc5732f7", # Insert appropriate client secret
        redirect_uri=url_for('redirectPage', _external=True),
        scope=["user-library-read", "playlist-modify-private"]
    )

# Helper Functions
def get_token():
    """
        Get the Spotify access token from the session data or refresh it if it has expired.

        Returns:
            dict: Token information including the access token.
    """
    token_info = session.get(TOKEN_INFO)
    if not token_info:
        raise Exception("Token not found!")

    now = int(time.time())
    if token_info['expires_at'] - now < 60:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info



def get_playlist_tracks(playlist_choice, playlist_length):
    """
    Retrieve track IDs for a Spotify playlist and add them to the 'ids' list.

    Args:
        playlist_choice (str): Spotify playlist URL.
        playlist_length (int): Desired length of the playlist.

    Globals:
        ids (list): List to store track IDs.
        url_error (bool): Indicates if there's an issue with the playlist URL.

    Returns:
        None
    """
    global ids
    global url_error

    sp = spotipy.Spotify(auth=get_token()['access_token'])

    if(playlist_choice[0:12] != "https://open"): # Edit url if hyperlinks are used
        response = requests.head(playlist_choice, allow_redirects=True)
        playlist_choice = response.url

    # Extract the playlist ID from the URL
    start_index = playlist_choice.find("/playlist/") + len("/playlist/")
    end_index = playlist_choice.find("?", start_index)
    playlist_id = playlist_choice[start_index:end_index]

    try:
        # Attempt to retrieve the tracks from the playlist
        results = sp.playlist(playlist_id=playlist_id)['tracks']
    except:
        # Set 'url_error' to True if there's an issue with the playlist URL
        url_error = True
        return

    # Extract track IDs from the retrieved data
    track_ids = [item['track']['id'] for item in results['items'] if item['track']['id']]

    # Retrieve recommended tracks to complete the playlist

    while len(ids) < playlist_length:
        # Get a list of recent tracks from 'track_ids'
        seed_tracks = track_ids[-5:]

        # Set the limit to the minimum of playlist_length or 100
        limit = min(playlist_length, 100)

        # Get recommended tracks based on the recent tracks
        recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=limit)

        for track in recommendations['tracks']:
            # Add recommended track IDs to the 'ids' list
            ids.append(track['id'])

        # Remove the used track IDs from 'track_ids'
        track_ids = track_ids[:-5]

    # Trim the 'ids' list to match 'playlist_length'
    if len(ids) > playlist_length:
        ids = ids[:playlist_length]



def tracks_to_playlist(playlist_length, playlist_name):
    """
    Create a new Spotify playlist and add tracks from the 'ids' list to it.
    Correct user ID must be added.

    Args:
        playlist_length (int): Desired length of the new playlist.
        playlist_name (str): Name for the new playlist.

    Globals:
        ids (list): List of track IDs to add to the playlist.

    Returns:
        None
    """
    global ids


    # Trim 'ids' list if it's longer than the desired playlist length
    if len(ids) < playlist_length:
        ids = ids[:playlist_length]

    sp = spotipy.Spotify(auth=get_token()['access_token'])

    user_id = sp.me()['id'] # Retrieves user id

    # Create a new private playlist with the specified name
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)['id']

    # Split 'ids' into chunks of 100 and add them to the new playlist
    chunk_size = 100
    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i + chunk_size]
        sp.playlist_add_items(playlist_id=playlist, items=chunk)


# Routes
@app.route('/redirect')
def redirectPage():
    """
    Handles the redirection from Spotify's authorization and stores the token information.

    Redirects the user to the 'user_input' route upon successful login.

    Returns:
        Flask response: Redirect to 'user_input' or an error message.
    """
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('user_input', _external=True))

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Route for the application's main page.

    If the user has a valid token, it redirects to the 'home' page; otherwise, it renders the login page.

    Returns:
        Flask response: Redirect or login page.
    """
    try:
        token_info = get_token()
        return redirect("/home")
    except Exception:
        print("not logged in")
        return render_template('login.html')  # Render the home.html template

@app.route('/login', methods=['GET', 'POST'])
def login_action():
    """
    Route for handling the login action.

    Redirects the user to the Spotify authorization URL.

    Returns:
        Flask response: Redirect to the Spotify authorization page.
    """
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)




@app.route('/home', methods=['GET', 'POST'])
def user_input():
    """
    Route for user input and playlist creation.

    If the user is logged in and submits a form, it collects input data and redirects to the playlist creation route.
    If the user is not logged in, it redirects to the login page.

    Returns:
        Flask response: Redirect or user input page.
    """
    try:
        token_info = get_token()
    except Exception:
        print("not logged in")
        return redirect("/")

    if request.method == 'POST':
        global playlist_choice
        global playlist_name
        global playlist_length
        playlist_choice = request.form.get('input1')
        playlist_name = request.form.get('input2')
        playlist_length = int(request.form.get('input3'))
        return redirect(url_for('make_playlist_csv', _external=True))
    return render_template('index.html')

@app.route('/newplaylist')
def make_playlist_csv():
    """
    Route for creating a new Spotify playlist.

    If the user is logged in and the playlist URL is valid, it creates the playlist.
    If the user is not logged in or the URL is invalid, it redirects accordingly.

    Returns:
        Flask response: Redirect with success or error message.
    """
    try:
        # Check if playlist_choice is defined, and if not, it will raise a NameError
        playlist_choice
    except NameError:
        # Redirect to /home if playlist_choice is not defined
        return redirect("/")

    try:
        token_info = get_token()
    except Exception:
        print("not logged in")
        return redirect("/")

    global url_error

    get_playlist_tracks(playlist_choice, playlist_length)
    if(url_error):
        return redirect('/home?message=Invalid+playlist+URL.')
    tracks_to_playlist(playlist_length, playlist_name)
    return redirect('/home?message=Playlist+created+successfully!')

@app.route('/about')
def about():
    """
    Route for displaying the 'About' page.

    Returns:
        Flask response: About page.
    """
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    """
    Route for displaying the 'Privacy Policy' page.

    Returns:
        Flask response: Privacy Policy page.
    """
    return render_template('privacy.html')

if __name__ == '__main__': # Run app
    app.run(debug=False)



