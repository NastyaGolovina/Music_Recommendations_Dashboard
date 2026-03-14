import streamlit as st
import pandas as pd
from data_loader import load_music


def user_dashboard():
    st.title("User Dashboard")

    with st.spinner("Loading music data..."):
        music = load_music()

    c1, c2, c3, c4 = st.columns(4)




    c1.metric("Songs", music["title"].nunique(), border=True)
    c2.metric("Artists", music["artist"].nunique(), border=True)
    c3.metric("Regions", music["region"].nunique(), border=True)
    c4.metric("streams", "...", border=True)
