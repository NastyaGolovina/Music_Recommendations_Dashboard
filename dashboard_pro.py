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


        r3, r4 = st.columns([2, 3], border=True)
        with r3:
            st.subheader("📊 Market Overview")

            # toggle between views
            view = st.radio("View by", ["Genre", "Artist", "Song"], horizontal=True, key="pro_view")

            # filters
            p1, p2, p3 = st.columns(3)

            pro_copy = music.copy()
            pro_copy["date"] = pd.to_datetime(pro_copy["date"])
            pro_copy["year"] = pro_copy["date"].dt.year

            selected_year = p1.selectbox("Year",
                                         ["All"] + sorted(pro_copy["year"].dropna().unique().astype(int).tolist()),
                                         key="pro_year")
            selected_region = p2.selectbox("Region", ["Global"] + sorted(
                pro_copy[pro_copy["region"] != "Global"]["region"].unique().tolist()), key="pro_region")
            top_n = p3.selectbox("Top", [5, 10, 20], key="pro_topn")

            # apply filters
            filtered = pro_copy.copy()
            if selected_year != "All":
                filtered = filtered[filtered["year"] == int(selected_year)]
            if selected_region != "Global":
                filtered = filtered[filtered["region"] == selected_region]

            # group by selected view
            if view == "Genre":
                col = "main_genre"
            elif view == "Artist":
                col = "artist"
            else:
                col = "title"

            grouped = (
                filtered.groupby(col)["streams"]
                .sum()
                .sort_values(ascending=False)
                .head(top_n)
                .reset_index()
            )

            # pie chart
            fig = px.pie(
                grouped,
                names=col,
                values="streams",
                hole=0.3,
            )

            fig.update_layout(
                height=450,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True,
            )

            st.plotly_chart(fig, use_container_width=True)
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
