import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


# reads a given csv file
def read_movies_file(file_name):
    return pd.read_csv(file_name, "::")


# reads second csv file to be joined in the future.
def read_rating_file(file_name):
    return pd.read_csv(file_name, "::")


if __name__ == '__main__':
    # Get project directory
    ROOT_DIR = str(Path(__file__).parent.parent)

    # Prepare file paths
    movie_file_name = ROOT_DIR + "/InputFiles/movies.dat"
    rating_file_name = ROOT_DIR + "/InputFiles/ratings.dat"

    # Read file into pandas dataframe
    movies_df = read_movies_file(movie_file_name)

    # Read ratings file into pandas dataframe
    ratings_df = read_rating_file(rating_file_name)

    # for debug only
    # pd.set_option('display.max_columns', None)

    # Join both the dataframes,
    join_df = movies_df.join(ratings_df.set_index('MovieID'), on='MovieID')[['Title', 'Rating']]

    # Calculate the average rating for each movie by grouping the movie name
    # defining the variables 'rating','title','rating'
    # Sort dataframe by the rating
    # Take first 100 movies
    top100_df = join_df \
                    .groupby('Title') \
                    .agg(Rating=('Rating', 'mean'), Count=('Title', 'size'), Total=('Rating', 'sum')) \
                    .query('Count > 10') \
                    .sort_values(by='Count', ascending=False) \
        [:100]

    # Write the data into CSV file
    top100_df.to_csv(ROOT_DIR + "/Output/Top100RatedMovies.csv")

    #   create a new dataframe, now  including 'genres' data.
    genres_rating_df = movies_df.join(ratings_df.set_index('MovieID'), on='MovieID')[['Genres', 'Rating']]
    print(genres_rating_df)
    #   separates the given genres from its grouped form to individual pieces.
    #   group by the genres
    #   defines rating as the average of the ratings.
    #   sorts them
    plt_df = genres_rating_df.assign(Genres=genres_rating_df['Genres'].str.split('|')) \
        .explode('Genres') \
        .groupby('Genres') \
        .agg(Rating=('Rating', 'mean')) \
        .sort_values(by='Rating', ascending=False)

    print(plt_df)

    # show the graph
    plt_df.reset_index().plot.bar(x='Genres', color='red')
    plt.tight_layout()
    plt.show()
