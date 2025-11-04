import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_movie(selected_title, n=5):
    # Load data
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")

    # Create user–movie matrix
    matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

    # Compute similarity between movies
    similarity = cosine_similarity(matrix.T)
    sim_df = pd.DataFrame(similarity, index=matrix.columns, columns=matrix.columns)

    # Get selected movieId
    try:
        movie_id = movies.loc[movies['title'] == selected_title, 'movieId'].values[0]
    except IndexError:
        return pd.DataFrame()

    # Find similar movies
    similar_scores = sim_df[movie_id].sort_values(ascending=False).iloc[1:n+1]
    recommended_ids = similar_scores.index
    recommendations = movies[movies['movieId'].isin(recommended_ids)]

    return recommendations[['title', 'genres']]
