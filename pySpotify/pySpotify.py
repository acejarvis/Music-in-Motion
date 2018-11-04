
#  pySpotify
#
#  Created by Jarvis Wang on 2018-11-03.
#  Copyright © 2018 Jarvis Wang. All rights reserved.
# 


#UTRA Hacks 2018
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username
# username = sys.argv[1]

# User ID: acejarvis

# Erase cache and prompt for user permission
username = 'zack_manesiotis'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
client_id = '5a697a22138740e8ab30ce2ef839f3d8'
client_secret = '88600ca366214c25842d44d0a21af53d'
redirect_uri = 'http://apple.com/'


try:
    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    # token = util.prompt_for_user_token(username,scope)
except(AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    # token = util.prompt_for_user_token(username,scope)
    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)


# Create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

# Get current device
devices = spotifyObject.devices()
print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id'] #where change the deviceID

# Current track information
track = spotifyObject.current_user_playing_track()
print(json.dumps(track, sort_keys=True, indent=4))
print()

artist = track['artists']['items'][0]
track = track['item']['name']
 
if artist != "":
    print("Currently playing " + artist + " - " + track)





# User information
user = spotifyObject.current_user()
displayName = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print(">>> Welcome to Spotipy " + displayName + "!")
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("1 - Search for an artist")
    print("0 - exit")
    print()
    choice = input("Your choice: ")

    # Search for the artist
    if choice == "1":
        print()
        searchQuery = input("Artist's Name:")
        print()

        # Get search results
        searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")
        print(json.dumps(searchResults, sort_keys=True, indent=4))

        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']


        # Album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM: " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

        # See album art
        while True:
            songSelection = input("Enter a song number to see album art and play the song (x to exit): ") # and play the song
            if songSelection == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIs[int(songSelection)])
            spotifyObject.start_playback(deviceID, None, trackSelectionList) # added
            webbrowser.open(trackArt[int(songSelection)])


    if choice == "0":
        break
