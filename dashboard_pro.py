import streamlit as st
from data_loader import load_music


def pro_dashboard():
    st.title("Professional Dashboard")
    st.write("Professional analytics here")

    with st.spinner("Loading music data..."):
        music = load_music()