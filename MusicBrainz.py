import requests
import pandas as pd
import time

# Load your CSV with one column "artist"
df = pd.read_csv("artists.csv")

def get_artist_genres(artist_name):
    """
    Returns a comma-separated string of genre-like tags for the artist
    """
    try:
        # Step 1: Search artist to get MBID
        search_url = "https://musicbrainz.org/ws/2/artist"
        params = {"query": artist_name, "fmt": "json"}
        headers = {"User-Agent": "GenreFetcher/1.0 ( 50405@alunos.upt.pt )"}
        r = requests.get(search_url, params=params, headers=headers)
        data = r.json()
        if "artists" not in data or len(data["artists"]) == 0:
            return None

        mbid = data["artists"][0]["id"]

        # Step 2: Lookup artist MBID with tags (genres)
        lookup_url = f"https://musicbrainz.org/ws/2/artist/{mbid}"
        params = {"inc": "tags", "fmt": "json"}
        r = requests.get(lookup_url, params=params, headers=headers)
        data = r.json()

        # Step 3: Extract genre-like tags
        if "tags" in data:
            genre_tags = [tag['name'] for tag in data["tags"]]
            return ", ".join(genre_tags) if genre_tags else None
        return None

    except Exception as e:
        print(f"Error for {artist_name}: {e}")
        return None

# Example: get genres for first 10 artists (for testing)
genres = []
for idx, artist in enumerate(df['artist'].head(10)):
    g = get_artist_genres(artist)
    genres.append(g)
    print(f"{idx+1}: {artist} -> {g}")
    time.sleep(1)  # Important: MusicBrainz free API limit = 1 request/sec

# Add genres column
df_test = df.head(10).copy()
df_test['genre'] = genres
df_test.to_csv("artists_with_genres_test.csv", index=False)
print("Done! Saved to artists_with_genres_test.csv")