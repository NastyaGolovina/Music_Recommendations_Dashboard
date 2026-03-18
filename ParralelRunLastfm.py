import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Semaphore
import threading
import os
import sys

# input_file = "artists_blocks/artists_part_6.csv"
# output_file = "artists_result/artists_part_6_with_genres.csv"
#
# API_KEY = "6f2eab9cb28d75263a464bac1c489a07"  # <-- paste API key here (not Shared secret)

# YOU CAN USE MY KEY TO RUN 2 OR 3 PARTS AT THE SAME TIME AND RUN IN TERMINAL WITH
# "python Lastfm.py number of your part, eg:15 & python Lastfm.py "number of your part, eg:15" &"
API_KEYS = [
    "8a0db88df4a73627b21555b7de9ac0d4",  # key 1 - use for part 20
    "77377a60eb5cd03bbcc0537c1cc44662",   # key 2 - use for part 21
   # "6f2eab9cb28d75263a464bac1c489a07",   # key 3 - use for part 22
]

part = int(sys.argv[1])
API_KEY = API_KEYS[part % len(API_KEYS)]

input_file = f"artists_blocks/artists_part_{part}.csv"
output_file = f"artists_results/artists_part_{part}_with_genres.csv"

df = pd.read_csv(input_file)

RATE_LIMIT = 0.2
semaphore = Semaphore(5)
last_request_time = [0.0]


def throttled_get(params):
    with semaphore:
        now = time.time()
        wait = RATE_LIMIT - (now - last_request_time[0])
        if wait > 0:
            time.sleep(wait)
        last_request_time[0] = time.time()
        return requests.get(
            "https://ws.audioscrobbler.com/2.0/",
            params=params,
            timeout=10
        )

def get_artist_genres(artist_name, retries=3):
    for attempt in range(retries):
        try:
            r = throttled_get({
                "method": "artist.getTopTags",
                "artist": artist_name,
                "api_key": API_KEY,
                "format": "json"
            })
            data = r.json()

            if "toptags" not in data or "tag" not in data["toptags"]:
                return artist_name, None

            tags = data["toptags"]["tag"]
            genres = [t["name"] for t in tags]
            return artist_name, ", ".join(genres) if genres else None

        except Exception as e:
            print(f"[Attempt {attempt+1}] Error for {artist_name}: {e}")
            time.sleep(2 ** attempt)

    return artist_name, None


# Cache — skip artists that are already fetched
results = {}
if os.path.exists(output_file):
    existing = pd.read_csv(output_file)
    done = existing[existing["genre"].notna()]
    results = dict(zip(done["artist"], done["genre"]))
    print(f"Already done: {len(results)} artists")

to_fetch = [a for a in df["artist"] if a not in results]
print(f"Remaining: {len(to_fetch)} artists\n")

# Run with 3 threads, print each result immediately
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(get_artist_genres, artist): artist for artist in to_fetch}
    for i, future in enumerate(as_completed(futures)):
        artist, genre = future.result()
        results[artist] = genre
        print(f"{i+1}: {artist} -> {genre}")

# Save
df["genre"] = df["artist"].map(results)
df.to_csv(output_file, index=False)
print(f"\nDone! Saved to {output_file}")