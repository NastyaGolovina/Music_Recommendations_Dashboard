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



    col_left, col_right = st.columns([2, 1] , border=True)

    with col_left:
        r1, r2 = st.columns([3, 2], border=True)
        with r1:
            st.subheader("Upper left left")
        with r2:
            st.subheader("Left upper right")

        r3, r4 = st.columns([1, 3], border=True)
        with r3:
            st.subheader("Left lower left")
        with r4:
            st.subheader("Left lower right")


    with col_right:
        st.subheader("Right column")
