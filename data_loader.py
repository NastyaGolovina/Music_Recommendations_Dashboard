import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_music():
    return pd.read_csv("music.csv")