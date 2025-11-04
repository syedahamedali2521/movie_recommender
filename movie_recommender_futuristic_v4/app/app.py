import sys
import os
import streamlit as st
import pandas as pd

# ✅ Fix import path for src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recommend import recommend_movie

# ------------------------------------------------
# ⚙️ Streamlit Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# 🎨 BLACK NEON THEME (FULL BACKGROUND FIX)
# ------------------------------------------------
st.markdown("""
<style>
/* 🌌 Global dark theme */
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid rgba(0, 255, 255, 0.2);
}

/* Text */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: #ffffff !important;
    font-family: 'Poppins', sans-serif;
}

/* Titles */
h1 {
    color: #00ffff !important;
    text-shadow: 0 0 25px #00ffff;
    text-align: center;
    font-size: 3em;
    margin-top: 10px;
}
h2 {
    color: #00ffff !important;
    text-shadow: 0 0 15px #00ffff;
    text-align: center;
    margin-top: 30px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00ffff, #ff00ff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    transition: 0.3s;
    font-size: 1rem;
    box-shadow: 0 0 10px #00ffff80;
}
.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 25px #ff00ff;
}

/* Movie Cards */
.movie-card {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 18px;
    padding: 1rem;
    margin: 1rem;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
}
.movie-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 30px #00ffff;
}

/* Divider and footer */
hr {
    border: 1px solid rgba(255,255,255,0.1);
}
footer, .css-164nlkn, .css-1q1n0ol {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 🎬 HEADER
# ------------------------------------------------
st.markdown("<h1>🎥 AI Movie Recommendation System</h1>", unsafe_allow_html=True)
st.write("### Experience futuristic AI-powered movie suggestions 🔮")

# ------------------------------------------------
# 📂 Load Movie Data
# ------------------------------------------------
movies_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'movies.csv')

if not os.path.exists(movies_path):
    st.error("⚠️ movies.csv not found in /data folder. Please ensure it's there.")
else:
    movies_df = pd.read_csv(movies_path)

# ------------------------------------------------
# 🎛️ Sidebar Controls
# ------------------------------------------------
st.sidebar.header("🎬 Choose a Movie")

if 'title' in movies_df.columns:
    selected_movie = st.sidebar.selectbox(
        "Select a movie you like:",
        movies_df['title'].values
    )

    n_recommendations = st.sidebar.slider("Number of recommendations", 3, 10, 5)

    if st.sidebar.button("🚀 Recommend"):
        st.markdown("<h2>✨ Top Recommended Movies ✨</h2>", unsafe_allow_html=True)

        try:
            recommendations = recommend_movie(selected_movie, n_recommendations)

            if isinstance(recommendations, pd.DataFrame) and not recommendations.empty:
                cols = st.columns(3)
                for idx, row in enumerate(recommendations.itertuples(), start=1):
                    with cols[(idx - 1) % 3]:
                        st.markdown(f"""
                        <div class='movie-card'>
                            <h3>{row.title}</h3>
                            <p style='color:#aaa;'>{row.genres}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No recommendations found for this movie.")
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.error("Invalid movie dataset structure. Ensure 'title' column exists in movies.csv")

# ------------------------------------------------
# 🪩 FOOTER
# ------------------------------------------------
st.markdown("""
<hr>
<p style='text-align:center; color:#888;'>Built by ❤️ Syed Ahamed Ali| © 2025 Futuristic Labs</p>
""", unsafe_allow_html=True)
