import streamlit as st
import pandas as pd
import numpy as np
import random

# Conf
st.set_page_config(
    page_title="Lyric Clusters",
    page_icon="🎵",
    layout="wide",
)

# Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0e0e0e;
    color: #e8e2d9;
}

h1, h2, h3 { font-family: 'DM Serif Display', serif; }

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

/* hero */
.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #2a2a2a;
    margin-bottom: 2.5rem;
}
.hero h1 {
    font-size: 3.2rem;
    letter-spacing: -0.02em;
    color: #e8e2d9;
    margin-bottom: 0.4rem;
}
.hero p {
    color: #7a7a7a;
    font-size: 1rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.05em;
}

/* cluster card */
.cluster-header {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #222;
}
.cluster-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #c8a96e;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.cluster-size {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #444;
}

/* song row */
.song-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 0.45rem 0;
    border-bottom: 1px solid #1a1a1a;
}
.song-row:last-child { border-bottom: none; }
.song-title {
    font-size: 0.9rem;
    font-weight: 500;
    color: #e8e2d9;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 55%;
}
.song-meta {
    font-size: 0.78rem;
    color: #555;
    font-family: 'DM Mono', monospace;
    text-align: right;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 44%;
}

/* search result */
.result-card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.6rem;
}
.result-rank {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #c8a96e;
    letter-spacing: 0.12em;
    margin-bottom: 0.3rem;
}
.result-title {
    font-size: 1rem;
    font-weight: 500;
    color: #e8e2d9;
}
.result-artist {
    font-size: 0.82rem;
    color: #666;
    margin-top: 0.1rem;
}
.result-genre {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #3a3a3a;
    margin-top: 0.4rem;
}

/* tab styling override */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #222;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #555;
    padding: 0.6rem 1.4rem;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #c8a96e !important;
    border-bottom: 2px solid #c8a96e !important;
    background: transparent !important;
}

/* search input */
.stTextInput > div > div > input {
    background: #141414;
    border: 1px solid #2a2a2a;
    color: #e8e2d9;
    font-family: 'DM Sans', sans-serif;
    border-radius: 6px;
    padding: 0.6rem 1rem;
}
.stTextInput > div > div > input:focus {
    border-color: #c8a96e;
    box-shadow: 0 0 0 1px #c8a96e22;
}

/* selectbox */
.stSelectbox > div > div {
    background: #141414;
    border: 1px solid #2a2a2a;
    color: #e8e2d9;
    border-radius: 6px;
}

/* metric */
[data-testid="stMetric"] {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 8px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #555 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem !important;
    color: #e8e2d9 !important;
}

.stButton > button {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    color: #e8e2d9;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    border-radius: 6px;
    padding: 0.4rem 1rem;
}
.stButton > button:hover {
    border-color: #c8a96e;
    color: #c8a96e;
}

/* divider */
hr { border-color: #1e1e1e; }
</style>
""", unsafe_allow_html=True)


# Load Data
@st.cache_data
def load_data(path="/home/esa/projects/lyrics-dataset/clustered_meta.csv"):
    df = pd.read_csv(path)
    df["cluster"] = df["cluster"].astype(int)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("clustered_meta.csv not found. Place it in the same directory as app.py.")
    st.stop()

n_clusters = df["cluster"].nunique()
cluster_ids = sorted(df["cluster"].unique())

# Title
st.markdown("""
<div class="hero">
    <h1>Lyric Clusters</h1>
</div>
""", unsafe_allow_html=True)

# Cluster Stats
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Songs", f"{len(df):,}")
m2.metric("Clusters", n_clusters)
m3.metric("Avg Cluster Size", f"{len(df) // n_clusters}")
m4.metric("Embedding Dim", "64")

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["CLUSTER EXPLORER", "SONG SEARCH"])


# Tab 1
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    cols_per_row = 3
    rows = [cluster_ids[i:i+cols_per_row] for i in range(0, len(cluster_ids), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row, gap="large")
        for col, cid in zip(cols, row):
            cluster_df = df[df["cluster"] == cid]
            sample = cluster_df.sample(min(5, len(cluster_df)), random_state=random.randint(0, 9999))
            size = len(cluster_df)

            with col:
                st.markdown(f"""
                <div class="cluster-header">
                    <span class="cluster-num">Cluster {cid}</span>
                    <span class="cluster-size">{size} songs</span>
                </div>
                """, unsafe_allow_html=True)

                for _, row_data in sample.iterrows():
                    song = str(row_data.get("song_name", "—"))
                    artist = str(row_data.get("artist_name", "—"))
                    genre_raw = str(row_data.get("genres", ""))
                    # take first genre tag only
                    genre = genre_raw.split(";")[0].strip() if genre_raw else "—"

                    st.markdown(f"""
                    <div class="song-row">
                        <span class="song-title">{song}</span>
                        <span class="song-meta">{artist} · {genre}</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔀  Resample all clusters"):
        st.rerun()

# Tab 2
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    search_col, info_col = st.columns([1, 1], gap="large")
    selected = None
    mask = pd.Series([False] * len(df))
    matches = pd.DataFrame()
    song_options = []
    selected_idx = None
    selected_row = None
    selected_cluster = None

    with search_col:
        query = st.text_input("Search for a song or artist", placeholder="e.g. dear god, eminem")

        if query:
            mask = df["song_name"].str.lower().str.contains(query.lower(), na=False) | df["artist_name"].str.lower().str.contains(query.lower(), na=False)
            matches = df[mask]

            if matches.empty:
                st.markdown("<p style='color:#555;font-size:0.85rem;'>No songs found.</p>", unsafe_allow_html=True)
            else:
                # in case of multiple matches
                song_options = (matches["song_name"] + " — " + matches["artist_name"]).tolist()
                selected = st.selectbox("Select a song", song_options)

                selected_idx = song_options.index(selected)
                selected_row = matches.iloc[selected_idx]
                selected_cluster = int(selected_row["cluster"])

                st.markdown(f"""
                <div style='margin-top:1.2rem;'>
                    <div style='font-family:DM Mono,monospace;font-size:0.7rem;color:#c8a96e;letter-spacing:0.1em;margin-bottom:0.3rem;'>SELECTED</div>
                    <div style='font-size:1.1rem;font-weight:500;'>{selected_row['song_name']}</div>
                    <div style='font-size:0.85rem;color:#666;'>{selected_row['artist_name']}</div>
                    <div style='font-family:DM Mono,monospace;font-size:0.7rem;color:#444;margin-top:0.5rem;'>
                        cluster {selected_cluster} · {selected_row.get('genres','').split(';')[0].strip()}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with info_col:
        if selected:
            cluster_songs = df[df["cluster"] == selected_cluster]
            cluster_songs = cluster_songs[cluster_songs["song_name"] != selected_row["song_name"]]
            neighbors = cluster_songs.sample(min(8, len(cluster_songs)), random_state=42)

            st.markdown(f"""
            <div style='font-family:DM Mono,monospace;font-size:0.7rem;color:#555;letter-spacing:0.1em;margin-bottom:1rem;'>
                {len(cluster_songs)} OTHER SONGS IN CLUSTER {selected_cluster}
            </div>
            """, unsafe_allow_html=True)

            for rank, (_, nb) in enumerate(neighbors.iterrows(), 1):
                song = str(nb.get("song_name", "—"))
                artist = str(nb.get("artist_name", "—"))
                genre = str(nb.get("genres", "")).split(";")[0].strip()

                st.markdown(f"""
                <div class="result-card">
                    <div class="result-rank">#{rank:02d}</div>
                    <div class="result-title">{song}</div>
                    <div class="result-artist">{artist}</div>
                    <div class="result-genre">{genre}</div>
                </div>
                """, unsafe_allow_html=True)
        elif not query:
            st.markdown("""
            <div style='color:#333;font-size:0.85rem;padding-top:2rem;'>
                Search for a song on the left to see other songs in its cluster.
            </div>
            """, unsafe_allow_html=True)