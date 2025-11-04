import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
def create_user_movie_matrix(ratings):
    matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    return matrix
def get_movie_recommendations(movie_id, ratings, movies, top_n=6):
    matrix = create_user_movie_matrix(ratings)
    if movie_id not in matrix.columns:
        return pd.DataFrame([])
    sim = cosine_similarity(matrix.T)
    sim_df = pd.DataFrame(sim, index=matrix.columns, columns=matrix.columns)
    scores = sim_df[movie_id].drop(labels=[movie_id]).sort_values(ascending=False)
    top = scores.head(top_n).index.tolist()
    return movies[movies['movieId'].isin(top)].assign(score=scores[top].values)
