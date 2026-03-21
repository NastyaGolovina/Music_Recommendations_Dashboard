import streamlit as st
import pandas as pd
from data_loader import load_data
import plotly.express as px


@st.cache_data
def get_metrics(music):
    return {
        "songs": music["title"].nunique(),
        "artists": music["artist"].nunique(),
        "regions": music["region"].nunique(),
        "streams": music["streams"].sum()
    }


def user_dashboard():
    st.title("User Dashboard")

    # with st.spinner("Loading music data..."):
    #     music = load_music()
    #
    # with st.spinner("Loading ganers data..."):
    #         genres = load_genre()
    with st.spinner("Loading data..."):
            music = load_data()

    m = get_metrics(music)

    c1, c2, c3, c4 = st.columns(4)


    # c1.metric("Songs", music["title"].nunique(), border=True)
    # c2.metric("Artists", music["artist"].nunique(), border=True)
    # c3.metric("Regions", music["region"].nunique(), border=True)
    # c4.metric("streams", music['streams'].sum(), border=True)


    c1.metric("Songs", m["songs"], border=True)
    c2.metric("Artists", m["artists"], border=True)
    c3.metric("Regions", m["regions"], border=True)
    c4.metric("Streams", m['streams'] , border=True)


    col_left, col_right = st.columns([1, 2] , border=True)

    with col_left:

        st.subheader("Top of songs")
        sorted_songs_titles = music.copy()

        top_song_col_left, top_song_col_right = st.columns([1, 2])

        top_song = top_song_col_left.selectbox("Top", [5,10,20,100])

        col1, col2, col3 = st.columns(3)

        sorted_songs_titles["date"] = pd.to_datetime(sorted_songs_titles["date"])
        with col1:
            d = st.date_input(
                "Duration",
                value=(sorted_songs_titles["date"].min().date(), sorted_songs_titles["date"].max().date()),
                min_value=sorted_songs_titles["date"].min().date(),
                max_value=sorted_songs_titles["date"].max().date(),
                format="DD.MM.YYYY",
            )

        region = col2.selectbox(
            "Region",
            ["Global"] + sorted_songs_titles[sorted_songs_titles["region"] != "Global"]["region"].unique().tolist()
        )

        genre = col3.selectbox("Genre", ["All"] + sorted_songs_titles["main_genre"].unique().tolist())


        if len(d) == 2:
            sorted_songs_titles = sorted_songs_titles[
                (sorted_songs_titles["date"] >= pd.Timestamp(d[0])) &
                (sorted_songs_titles["date"] <= pd.Timestamp(d[1]))
                ]

        sorted_songs_titles = sorted_songs_titles[sorted_songs_titles["region"] == region]


        if genre != "All":
            sorted_songs_titles = sorted_songs_titles[sorted_songs_titles["main_genre"] == genre]



        sorted_songs_titles = (
            sorted_songs_titles.groupby("title", as_index=False)["streams"]
            .sum()
            .sort_values(by="streams", ascending=False)
        )

        fig = px.bar(
            sorted_songs_titles.head(top_song),
            x="streams",
            y="title",
            orientation="h",
            color_discrete_sequence=["#6b068a"]
            # ,title="Top Songs by Streams"
            # ,hover_data = {
            #     "title": False,  # убрать title (уже видно на оси)
            #     "streams": True,  # показать streams
            #     "artist": True,  # добавить исполнителя
            # }
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            yaxis_title="",
            xaxis_title="Streams",
            xaxis=dict(tickangle=-45)
        )

        st.plotly_chart(fig, use_container_width=True)


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