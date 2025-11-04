from src.recommend import recommend_movie
import pandas as pd

def display_recommendations(movie_id: int):
    try:
        recommendations = recommend_movie(movie_id)
        if isinstance(recommendations, pd.DataFrame) and not recommendations.empty:
            print(recommendations[['movieId','title','genres']].to_string(index=False))
        else:
            print('No recommendations available.')
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    print('Neon AI Movie Recommender CLI')
    try:
        movie_id = int(input('Enter Movie ID: '))
        display_recommendations(movie_id)
    except Exception as e:
        print('Invalid input.')
