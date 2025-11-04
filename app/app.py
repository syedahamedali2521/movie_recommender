import streamlit as st
import os
import sys
import pandas as pd


# ✅ Dynamically find project root and add 'src' to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, "src")

if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from recommend import recommend_movie
except Exception as e:
    st.error(f"❌ Import failed: {e}")
    st.stop()


# ==========================================================
# ⚙️ Streamlit Page Configuration
# ==========================================================
st.set_page_config(
    page_title="🎬 AI Movie Recommendation System",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# 🎨 Custom CSS (Dark Futuristic Theme)
# ==========================================================
st.markdown("""
<style>
    /* General background */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at top left, #00ffff20, #000000 80%);
        color: #00ffff;
        font-family: 'Poppins', sans-serif;
    }

    /* Header Text */
    h1, h2, h3, h4 {
        color: #00e0ff;
        text-shadow: 0px 0px 20px #00e0ff;
        font-weight: 700;
    }

    /* Streamlit widgets */
    .stSelectbox label, .stSlider label, .stNumberInput label {
        color: #00e0ff !important;
        font-weight: bold;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #00ffff, #0077ff);
        color: black;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 10px #00ffff;
    }
    div.stButton > button:hover {
        transform: scale(1.08);
        box-shadow: 0 0 30px #00ffff;
    }

    /* Movie Cards */
    .movie-card {
        background-color: rgba(0, 0, 0, 0.85);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        color: #00ffff;
        box-shadow: 0px 0px 20px #00ffff60;
        transition: 0.3s;
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 40px #00ffff;
    }

    /* Footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 🎬 Load Movie & Rating Data
# ==========================================================
movies_path = os.path.join(project_root, "data", "movies.csv")
# Correct dataset paths after flattening
movies_path = os.path.join(project_root, "data", "movies.csv")
ratings_path = os.path.join(project_root, "data", "ratings.csv")

# Stop if data files are missing
if not os.path.exists(movies_path) or not os.path.exists(ratings_path):
    st.error("⚠️ Missing dataset! Please make sure 'movies.csv' and 'ratings.csv' exist inside the 'data' folder.")
    st.stop()

# Load data
movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)


# ==========================================================
# 🧠 App Header
# ==========================================================
st.markdown("<h1 style='text-align:center;'>🤖 AI Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>🎞 Experience futuristic AI-powered movie suggestions 🎬</h3>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🎞 Sidebar Controls
# ==========================================================
with st.sidebar:
    st.header("🎥 Choose a Movie")
    selected_movie = st.selectbox("Select the movie you like 👇", movies['title'].values)
    top_n = st.slider("Number of recommendations:", 3, 10, 5)
    recommend_btn = st.button("🚀 Recommend")

# ==========================================================
# 💡 Main Recommendation Section
# ==========================================================
if recommend_btn:
    with st.spinner("🎯 Finding the best movie matches for you..."):
        try:
            recommendations = recommend_movie(selected_movie, movies, ratings, top_n=top_n)
            if recommendations.empty:
                st.warning("⚠️ No similar movies found! Try another title.")
            else:
                st.subheader("✨ Your Top Recommended Movies ✨")

                cols = st.columns(3)
                for i, (_, row) in enumerate(recommendations.iterrows()):
                    with cols[i % 3]:
                        st.markdown(
                            f"""
                            <div class='movie-card'>
                                <h4>{row['title']}</h4>
                                <p>{row['genres']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        except Exception as e:
            st.error(f"❌ Error while generating recommendations: {e}")

# ==========================================================
# 💬 Footer
# ==========================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray;'>Built by ❤️ Syed Ahamed Ali| © 2025 AIML Project</p>",
    unsafe_allow_html=True
)
