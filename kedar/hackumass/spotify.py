import json 
import spotipy 
import webbrowser
import os
username = os.environ['SP_USERNAME'] 
clientID = os.environ['SPCLIENTID']
clientSecret = os.environ['SPCLIENTSECRET'] 
redirect_uri = 'http://google.com/callback/'
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
token_dict = oauth_object.get_access_token() 
scope = "user-read-playback-state,user-modify-playback-state"

token = token_dict['access_token'] 
spotifyObject =  spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
          client_id=clientID,
          client_secret=clientSecret,
          redirect_uri=redirect_uri,    
          scope=scope, open_browser=False))
user_name = spotifyObject.current_user() 
# To print the response in readable format. 
print(json.dumps(user_name, sort_keys=True, indent=4)) 
while True: 
    print("Welcome to the project, " + user_name['display_name']) 
    print("0 - Exit the console") 
    print("1 - Search for a Song") 
    user_input = int(input("Enter Your Choice: ")) 
    if user_input == 1: 
        search_song = input("Enter the song name: ") 
        results = spotifyObject.search(search_song, 1, 0, "track") 
        songs_dict = results['tracks'] 
        song_items = songs_dict['items'] 
        song = song_items[0]['external_urls']['spotify'] 
        print("Song", song)
        songsplit = song.split('/')[-1]
        urisplit = spotifyObject.currently_playing().get('item').get('uri').split(':')[-1]

        if (songsplit != urisplit):
            spotifyObject.start_playback(uris=[song])
    elif user_input == 0: 
        print("Good Bye, Have a great day!") 
        break
    else: 
        print("Please enter valid user-input.") 
