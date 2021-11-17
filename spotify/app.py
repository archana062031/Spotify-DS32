import os
from flask import Flask, render_template, request
from .spotify import *
from .models import *
import pandas as pd
import sys

"""Create and configure an instance of the flask application"""
app = Flask(__name__)


# Configure app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
DB.init_app(app)

# Create table(s)
with app.app_context():
    DB.create_all()

# Root route


@app.route("/", methods=["GET", "POST"])
def root():
    """Base view"""

    return render_template("base.html", title="Song Recommender")


@app.route("/recommendations", methods=["GET", "POST"])
def recommendations_page():
    if request.method == "POST":
        song_name = request.form["song_name"]
        artist_name = request.form["artist_name"]

        try:
            song_id, artist_id = retrieve_spotify_ids(song_name, artist_name)
        except:
            message = "There was an error finding your song. Please go back and enter another song."
            # return render_template("recommendations.html", message=message)
            return "error" + sys.exc_info()[0]

        audio_features_dict = retrieve_audio_features(song_id)

        danceability = audio_features_dict[0]["danceability"]
        energy = audio_features_dict[0]["energy"]
        key = audio_features_dict[0]["key"]
        loudness = audio_features_dict[0]["loudness"]
        mode = audio_features_dict[0]["mode"]
        speechiness = audio_features_dict[0]["speechiness"]
        acousticness = audio_features_dict[0]["acousticness"]
        instrumentalness = audio_features_dict[0]["instrumentalness"]
        liveness = audio_features_dict[0]["liveness"]
        valence = audio_features_dict[0]["valence"]
        tempo = audio_features_dict[0]["tempo"]
        duration_ms = audio_features_dict[0]["duration_ms"]
        time_signature = audio_features_dict[0]["time_signature"]

        user_song_features = [
            danceability,
            energy,
            key,
            loudness,
            mode,
            speechiness,
            acousticness,
            instrumentalness,
            liveness,
            valence,
            tempo,
            duration_ms,
            time_signature,
        ]

        # Use function from model.py to get recommendations
        recommendations = find_recommendations(user_song_features)

        return render_template("recommendations.html", title="Recommendations", recommendations=recommendations, inputSongName=song_name, inputArtistName=artist_name)

    @app.route('/reset')
    def reset():
        # remove everything from the database
        DB.drop_all()
        # Creates the database file initially.
        DB.create_all()
        # return render_template('base.html', title='Reset Database')
        return "Reset Database"


if __name__ == "__main__":
    app.run()
