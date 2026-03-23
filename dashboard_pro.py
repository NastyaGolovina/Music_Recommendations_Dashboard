import streamlit as st
from data_loader import load_data
import pandas as pd
import plotly.express as px
import altair as alt




@st.cache_data
def get_metrics(music):
    return {
        "songs": music["title"].nunique(),
        "artists": music["artist"].nunique(),
        "regions": music["region"].nunique(),
        "streams": music["streams"].sum()
    }



def pro_dashboard():
    st.title("Professional Dashboard")

    # with st.spinner("Loading music data..."):
    #     music = load_music()
    #
    # c1, c2, c3, c4 = st.columns(4)
    #
    # c1.metric("Songs", music["title"].nunique(), border=True)
    # c2.metric("Artists", music["artist"].nunique(), border=True)
    # c3.metric("Regions", music["region"].nunique(), border=True)
    # c4.metric("streams", music['streams'].sum(), border=True)


    with st.spinner("Loading data..."):
            music = load_data()

    m = get_metrics(music)

    c1, c2, c3, c4 = st.columns(4)


    c1.metric("Songs", m["songs"], border=True)
    c2.metric("Artists", m["artists"], border=True)
    c3.metric("Regions", m["regions"], border=True)
    c4.metric("Streams", m['streams'] , border=True)




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
            st.subheader("Ranking of songs")
            songs_ranking = music.copy()

            col1, col2, col3 = st.columns(3)

            songs_ranking["date"] = pd.to_datetime(songs_ranking["date"])

            song = col1.selectbox(
                "Song",
                ["Rockabye (feat. Sean Paul & Anne-Marie)"] +
                songs_ranking[
                    songs_ranking["title"] != "Rockabye (feat. Sean Paul & Anne-Marie)"
                ]["title"].unique().tolist()
            )
            with col2:
                d = st.date_input(
                    "Duration",
                    value=(songs_ranking["date"].min().date(), songs_ranking["date"].max().date()),
                    min_value=songs_ranking["date"].min().date(),
                    max_value=songs_ranking["date"].max().date(),
                    format="DD.MM.YYYY",
                )

            region = col3.selectbox(
                "Region",
                ["Global"] + songs_ranking[songs_ranking["region"] != "Global"]["region"].unique().tolist()
            )

            if len(d) == 2:
                songs_ranking = songs_ranking[
                    (songs_ranking["date"] >= pd.Timestamp(d[0])) &
                    (songs_ranking["date"] <= pd.Timestamp(d[1]))
                    ]

            songs_ranking = songs_ranking[songs_ranking["region"] == region]
            songs_ranking = songs_ranking[songs_ranking["title"] == song]

            songs_ranking = songs_ranking.sort_values(by='date', ascending=True)

            # st.line_chart(
            #     songs_ranking,
            #     x="date",
            #     y=["rank"],
            #     color=["#FF0000"],
            # )
            line = alt.Chart(songs_ranking).mark_line(color="#7777ff").encode(
                x="date:T",
                y=alt.Y("rank:Q", scale=alt.Scale(reverse=True), title="Rank")
            )

            # points = alt.Chart(songs_ranking).mark_point(color="#7777ff", size=80, filled=False).encode(
            points = alt.Chart(songs_ranking).mark_point(color="#7777ff", size=80, filled=True).encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("rank:Q", scale=alt.Scale(reverse=True))
            )

            st.altair_chart((line + points).interactive(), use_container_width=True)


    with col_right:
        st.subheader("Right column")
