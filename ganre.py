# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import pandas as pd
# import time
# import json
# import os
#
# # ── Spotify client ──
# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
#     client_id="a13c3a534c3343428116119ada2c33d0",
#     client_secret="a3730667995342d9973943fd84b621b5"
# ))
#
# # ── Load your CSV ──
# music = pd.read_csv("charts.csv")
#
# # ── Fetch genres (with cache) ──
# CACHE = "artist_genres.json"
#
# if os.path.exists(CACHE):
#     with open(CACHE, "r") as f:
#         artist_genres = json.load(f)
#     print(f"Loaded {len(artist_genres)} artists from cache.")
# else:
#     artist_genres = {}
#
# # Find artists not yet cached
# all_artists = music["artist"].str.split(",").explode().str.strip().unique()
# missing = [a for a in all_artists if a not in artist_genres]
# print(f"Fetching {len(missing)} artists from Spotify API...")
#
# for i, name in enumerate(missing):
#     try:
#         results = sp.search(q=name, type="artist", limit=1)
#         items = results["artists"]["items"]
#         if items:
#             genres = items[0]["genres"]
#             artist_genres[name] = genres[0] if genres else "unknown"
#         else:
#             artist_genres[name] = "unknown"
#     except Exception as e:
#         artist_genres[name] = "unknown"
#         print(f"Error: {name} → {e}")
#     time.sleep(0.1)
#
#     # Save every 100 artists in case it crashes midway
#     if i % 100 == 0:
#         with open(CACHE, "w") as f:
#             json.dump(artist_genres, f)
#         print(f"Progress: {i}/{len(missing)}")
#
# # Final save
# with open(CACHE, "w") as f:
#     json.dump(artist_genres, f)
#
# # ── Add genre column ──
# def assign_genre(artist_str):
#     for artist in [a.strip() for a in artist_str.split(",")]:
#         genre = artist_genres.get(artist, "unknown")
#         if genre != "unknown":
#             return genre
#     return "unknown"
#
# music["genre"] = music["artist"].apply(assign_genre)
#
# # ── Save new CSV ──
# music.to_csv("spotify_with_genre.csv", index=False)
# print("Done! Saved as spotify_with_genre.csv")
# print(music["genre"].value_counts().head(10))