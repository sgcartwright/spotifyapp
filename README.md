# Spotify Playlist Radio Generator

Spotify's removal of the Playlist Radio feature has made it increasingly challenging to discover new music related to a specific playlist. The current algorithm tends to recommend music that listeners are already familiar with. This simple application addresses this issue by generating new Playlist Radios for any playlist you desire, without bias toward your listening habits. 

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Roadmap](#roadmap)
- [Setup](#setup)
- [Credit](#credit)

## Getting Started

To embark on your journey with the Spotify Playlist Radio Generator, follow these steps:

## Prerequisites

Before diving into this application, ensure you have the following prerequisites installed:

- **Python**
- **Flask**
- **Spotipy**

## Installation

1. Clone this repository to your local machine.
2. Install the required Python libraries using pip:

    ```bash
    pip install Flask spotipy
    ```

3. Replace `'YOUR_SECRET_KEY'` in `app.secret_key` with a secure random string.
4. Replace `client_id` and `client_secret` in the `create_spotify_oauth` function with your Spotify API client ID and client secret.

## Usage

1. Visit the web application in your browser.
2. Click the "Log in with Spotify" button to log in and grant access to your Spotify account.
3. Enter a Spotify playlist URL, a new playlist name, and the desired playlist length.
4. Click "Generate Playlist" to create a new playlist.

## Features

- **Log in with your Spotify account.**
- **Create new Spotify playlists based on existing playlists.**
- **Customize the name and length of the new playlist.**
- **Handles Spotify user authentication and authorization.**
- **User friendly app interface**

## Roadmap

Future improvements and features may include:

- Adding option for artist radios
- Adding option for genre radios
- Adding option for playlists based on recent listening
- Creating public webpage

## Setup

This project comes with a `setup.py` file, enabling easy installation of the required packages. Simply use the `pip install` command to install the prerequisites.

## Credit

Initial OAuth authorization code, as well as setup.py, taken from https://github.com/JasonLeviGoodison/SpotifyToYoutubeMP3.
