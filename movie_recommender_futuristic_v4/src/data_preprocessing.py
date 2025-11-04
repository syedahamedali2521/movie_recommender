import pandas as pd
def load_data(data_dir='data'):
    movies = pd.read_csv(f'{data_dir}/movies.csv')
    ratings = pd.read_csv(f'{data_dir}/ratings.csv')
    return movies, ratings
