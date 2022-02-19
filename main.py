import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = "6b04c91a3305467f86d4315d52326608"
SPOTIPY_CLIENT_SECRET = "545d7517a8c6464385fb239d508ef65e"

user = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

s = spotipy.oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, "http://example.com",
                                scope="playlist-modify-private").get_cached_token()
#
a = spotipy.client.Spotify(
    auth="BQBSeZkkPmDHG8oLmh9qKFxPSYX6TGqqy_vMaryo5Eb6cIsHWxiSgHPPsQ3n2B4oSj9iUOm1DSIw49KC9Ur_VUJBdg64wMCveXHUgoHC77"
         "jnz4oRCoTml-tmZYxWUL1SxpTJ9yMBeYQKtZi2_7M6fgMOouLzrejLicP0arBQGqcksLgHDu0Gci0",
    client_credentials_manager=user, oauth_manager=s).current_user()

year = input("YYYY:\n")
month = input("MM:\n")
day = input("DD:\n")
date = f"{year}-{month}-{day}"

URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
all_songs = [song.getText().strip("\n") for song in soup.find_all(name="span",
                                                                  class_="c-label a-font-primary-bold-l"
                                                                         " u-font-size-32@tablet"
                                                                         " u-letter-spacing-0080@tablet")]
Titles = [title.getText().strip("\n") for title in soup.find_all(name="h3", class_="u-letter-spacing-0021",
                                                                 id="title-of-a-story")]
Titles = Titles[1::2]
Titles = Titles[1::2]

play = user.user_playlist_create("davidrivas2002", "Top 2016 Songs", False, True, "API Project")
uris = []
play_id = play["id"]
for song in Titles:
    try:
        search = user.search(q=f"track:{song} year:2016", type="track", limit=1)
        uri = search["tracks"]["items"][0]["uri"]
        uris.append(uri)
    except IndexError:
        print(f"The song:{song} is not in spotify")

play = user.playlist_add_items(playlist_id=play_id, items=uris, position=None)
