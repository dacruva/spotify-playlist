from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


print(r"""                          ,     
                      ,   |     
   _,,._              |  0'     
 ,'     `.__,--.     0'         
/   .--.        |           ,,, 
| [=========|==|==|=|==|=|==___]
\   "--"  __    |           ''' 
 `._   _,'  `--'                
    ""'     ,   ,0     ,        
hjm         |)  |)   ,'|        
  ____     0'   '   | 0'        
  |  |             0'           
 0' 0'""")

# Getting values from .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
endpoint = os.getenv("ENDPOINT")
rurl = os.getenv("RURL")
username = os.getenv("USERNAME")

# Getting list of songs for that date
date = input("Type a date to get a top 100 song of that day YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
songs_list_spans = soup.select("li ul li h3")
songs_names = [song.getText().strip() for song in songs_list_spans]

# Spotify authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=rurl,
        scope="playlist-modify-private",
        username=username,
        cache_path="token.txt",
        show_dialog=False
        )
    )

user_id = sp.current_user()["id"]

# Searching for songs by title
song_uris = []
year = date.split("-")[0]
for song in songs_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
# adding songs
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
