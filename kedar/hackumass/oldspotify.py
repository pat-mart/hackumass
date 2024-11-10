import json 
import spotipy 
import webbrowser 
import os

username = os.environ['SP_USERNAME'] 
clientID = "a8044650845e4575b1f3cc118730ccf7"
clientSecret = "09f4b5cbc6c949b4b8c6ae5798427642"
redirect_uri = 'http://google.com/callback/'
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
token_dict = oauth_object.get_access_token() 
token = token_dict['access_token'] 
spotifyObject = spotipy.Spotify(auth=token) 
user_name = spotifyObject.current_user() 

# To print the JSON response from 
# browser in a readable format. 
# optional can be removed 
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
		webbrowser.open(song) 
		print('Song has opened in your browser.') 
	elif user_input == 0: 
		print("Good Bye, Have a great day!") 
		break
	else: 
		print("Please enter valid user-input.")