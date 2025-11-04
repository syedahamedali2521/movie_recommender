import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_movie(selected_movie, movies, ratings, top_n=6):
    """
    Recommends movies similar to the selected movie based on user ratings.
    """

    # Merge ratings with movies
    movie_data = ratings.merge(movies, on='movieId')

    # Create pivot table: users as rows, movies as columns
    user_movie_matrix = movie_data.pivot_table(index='userId', columns='title', values='rating')

    # Fill missing ratings with 0
    user_movie_matrix = user_movie_matrix.fillna(0)

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(user_movie_matrix.T)
    similarity_df = pd.DataFrame(similarity_matrix, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

    # Handle invalid movie name
    if selected_movie not in similarity_df.columns:
        return pd.DataFrame(columns=['movieId', 'title', 'genres'])

    # Get similar movies
    similar_movies = similarity_df[selected_movie].sort_values(ascending=False)[1:top_n+1].index

    # Return movie info
    recommendations = movies[movies['title'].isin(similar_movies)][['movieId', 'title', 'genres']]
    return recommendations
