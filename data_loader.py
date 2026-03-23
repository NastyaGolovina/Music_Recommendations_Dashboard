import pandas as pd
import streamlit as st

# @st.cache_data(show_spinner=False)
# def load_music():
#     return pd.read_csv("music.csv")
#
# def load_genre():
#     return pd.read_csv("artists_merged_clean_NAN_to_pop.csv")


@st.cache_data(show_spinner=False)
def load_data():
    music = pd.read_csv("music.csv")
    genres = pd.read_csv("artists_merged_clean_NAN_to_pop.csv")

    # music["date"] = pd.to_datetime(music["date"])

    genres["main_genre"] = (
        genres["genre"]
        .str.split(",")
        .str[0]
        .str.strip()
        .str.lower()
    )

    music = music.merge(
        genres[["artist", "main_genre"]],
        on="artist",
        how="left"
    )


    return music