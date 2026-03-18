import streamlit as st
from data_loader import load_music


def pro_dashboard():
    st.title("Professional Dashboard")
    st.write("Professional analytics here")

    with st.spinner("Loading music data..."):
        music = load_music()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Songs", music["title"].nunique(), border=True)
    c2.metric("Artists", music["artist"].nunique(), border=True)
    c3.metric("Regions", music["region"].nunique(), border=True)
    c4.metric("streams", music['streams'].sum(), border=True)