from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#function for creating billboard playlist
def create_billboard_playlist():
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
    billboard_url = "https://www.billboard.com/charts/hot-100/" + date
    response = requests.get(url=billboard_url, headers=header)

    soup = BeautifulSoup(response.text, 'html.parser')
    song_names_spans = soup.select("li ul li h3")
    song_names = [song.getText().strip() for song in song_names_spans]

    song_uris = []
    year = date.split("-")[0]
    for song in song_names:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

    playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
    print(f"Created Billboard playlist: {playlist['name']}")

#function for creating genre
def create_genre_playlist():
    genres = {
        "1": "rock",
        "2": "pop",
        "3": "jazz",
        "4": "hip-hop",
        "5": "electronic",
        "6": "country",
        "7": "r&b",
        "8": "classical",
        "9": "reggae",
        "10": "blues",
        "11": "folk",
        "12": "metal",
        "13": "punk",
        "14": "indie",
        "15": "alternative"
    }

    print("\nAvailable genres:")
    for key, genre in genres.items():
        print(f"{key}. {genre.title()}")

    choice = input("Choose a genre (1-15): ")

    if choice not in genres:
        print("Invalid choice. Please run the program again.")
        return

    genre = genres[choice]

    song_uris = []
    offset = 0
    limit = 50

    while len(song_uris) < 50 and offset < 200:
        results = sp.search(q=f"genre:{genre}", type="track", limit=limit, offset=offset)
        tracks = results['tracks']['items']

        if not tracks:
            break

        for track in tracks:
            if len(song_uris) >= 50:
                break
            song_uris.append(track['uri'])

        offset += limit

    if song_uris:
        playlist = sp.user_playlist_create(user=user_id, name=f"{genre.title()} Playlist", public=False)
        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
        print(f"Created {genre} playlist with {len(song_uris)} songs: {playlist['name']}")
    else:
        print(f"No songs found for genre: {genre}")

# function for creating activity playlist
def create_activity_playlist():
    activities = {
        "1": ("workout", "high energy upbeat motivational"),
        "2": ("sleep", "calm relaxing ambient peaceful"),
        "3": ("morning walk", "uplifting cheerful acoustic indie"),
        "4": ("study", "focus instrumental lo-fi ambient"),
        "5": ("party", "dance pop electronic energetic"),
        "6": ("road trip", "classic rock indie alternative upbeat"),
        "7": ("chill", "chill downtempo lo-fi relaxed"),
        "8": ("running", "electronic pump up high energy fast")
    }

    print("\nAvailable activities:")
    for key, (activity, _) in activities.items():
        print(f"{key}. {activity.title()}")

    choice = input("Choose an activity (1-8): ")

    if choice not in activities:
        print("Invalid choice. Please run the program again.")
        return

    activity_name, search_terms = activities[choice]

    song_uris = []
    search_queries = [
        f"{search_terms}",
        f"playlist:{activity_name}",
        f"{activity_name} music"
    ]

    for query in search_queries:
        if len(song_uris) >= 50:
            break

        offset = 0
        while len(song_uris) < 50 and offset < 100:
            results = sp.search(q=query, type="track", limit=50, offset=offset)
            tracks = results['tracks']['items']

            if not tracks:
                break

            for track in tracks:
                if len(song_uris) >= 50:
                    break
                if track['uri'] not in song_uris:
                    song_uris.append(track['uri'])

            offset += 50

    if song_uris:
        playlist = sp.user_playlist_create(user=user_id, name=f"{activity_name.title()} Playlist", public=False)
        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris[:50])
        print(f"Created {activity_name} playlist with {len(song_uris[:50])} songs: {playlist['name']}")
    else:
        print(f"No songs found for {activity_name} activity")

def create_popularity_playlist():
    popularity_types = {
        "1": ("trending", "Popular songs from the last year", "year:2024"),
        "2": ("underrated", "Hidden gems with low popularity", ""),
        "3": ("classic hits", "Popular songs from 1980-2010", "year:1980-2010")
    }

    print("\nAvailable popularity types:")
    for key, (name, description, _) in popularity_types.items():
        print(f"{key}. {name.title()} - {description}")

    choice = input("Choose a popularity type (1-3): ")

    if choice not in popularity_types:
        print("Invalid choice. Please run the program again.")
        return

    playlist_type, description, year_filter = popularity_types[choice]
    song_uris = []

    if choice == "1":  # Trending
        results = sp.search(q=f"year:2024", type="track", limit=50)
        tracks = sorted(results['tracks']['items'], key=lambda x: x['popularity'], reverse=True)[:50]
        song_uris = [track['uri'] for track in tracks]

    elif choice == "2":  # Underrated
        offset = 0
        while len(song_uris) < 50 and offset < 500:
            results = sp.search(q="genre:indie OR genre:alternative", type="track", limit=50, offset=offset)
            tracks = results['tracks']['items']

            underrated_tracks = [track for track in tracks if track['popularity'] < 50]
            for track in underrated_tracks:
                if len(song_uris) >= 50:
                    break
                if track['uri'] not in song_uris:
                    song_uris.append(track['uri'])
            offset += 50

    elif choice == "3":  # Classic hits
        search_years = ["1980", "1985", "1990", "1995", "2000", "2005", "2010"]
        for year in search_years:
            if len(song_uris) >= 50:
                break
            results = sp.search(q=f"year:{year}", type="track", limit=20)
            tracks = sorted(results['tracks']['items'], key=lambda x: x['popularity'], reverse=True)
            for track in tracks[:7]:
                if len(song_uris) >= 50:
                    break
                song_uris.append(track['uri'])

    if song_uris:
        playlist = sp.user_playlist_create(user=user_id, name=f"{playlist_type.title()} Playlist", public=False)
        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
        print(f"Created {playlist_type} playlist with {len(song_uris)} songs: {playlist['name']}")
    else:
        print(f"No songs found for {playlist_type} playlist")

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=YOUR-CLIENT-ID,
        client_secret=YOUR-CLIENT-SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# Main menu
print("Welcome to Playlist Creator!")
print("1. Create Billboard Hot 100 playlist")
print("2. Create genre-based playlist")
print("3. Create activity-based playlist")
print("4. Create popularity-based playlist")

choice = input("Choose an option (1, 2, 3, or 4): ")

if choice == "1":
    create_billboard_playlist()
elif choice == "2":
    create_genre_playlist()
elif choice == "3":
    create_activity_playlist()
elif choice == "4":
    create_popularity_playlist()
else:
    print("Invalid choice. Please run the program again.")
