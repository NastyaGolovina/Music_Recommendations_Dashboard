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
    c4.metric("streams", music['streams'].sum(), border=True)


    col_left, col_right = st.columns([1, 2] , border=True)

    with col_left:
        st.subheader("Left column")

    with col_right:

        r1, r2 = st.columns([3, 2], border=True)
        with r1:
            st.subheader("Upper right left")
        with r2:
            st.subheader("Right upper right")


        r3, r4 = st.columns([5, 6], border=True)
        with r3:
            st.subheader("Right lower left")
        with r4:
            st.subheader("Right lower right")