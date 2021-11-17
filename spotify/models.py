from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pickle

DB = SQLAlchemy()


class Recommendations(DB.Model):
    """
    Creates a Recommendations Table with SQlAlchemy.
    This is useful for jinja2 HTML formatting in the 'recommendations.html' file.
    """

    id = DB.Column(DB.BigInteger, primary_key=True)
    artist_song = DB.Column(DB.String, nullable=False)


def find_recommendations(input_feature_vector):
    # Load locally stored pickled model
    model = pickle.load(open('spotify/app_folder/Spotify_model_new', 'rb'))

    # Read in spotify data from csv
    songs = pd.read_csv("spotify/app_folder/song_artist.csv")

    # Query the model using the features from the user's selected song
    # Model will return the indices of the 10 most similar songs that it finds within the 100,000 rows
    dist, ind = model.kneighbors([input_feature_vector])

    # Convert 'indices' output from array type to list
    ind = list(ind[0])

    id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    artist_song = []

    for each in ind:
        artist_song.append(songs.iloc[each]["artists_song"])

    recommendations = list(zip(id_list, artist_song))

    return recommendations
