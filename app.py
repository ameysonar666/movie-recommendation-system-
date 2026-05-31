from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in distances:
        recommendations.append(
            movies.iloc[i[0]].title
        )

    return recommendations


@app.route("/", methods=["GET", "POST"])
def home():

    recommended_movies = []

    if request.method == "POST":

        selected_movie = request.form["movie"]

        recommended_movies = recommend(selected_movie)

    movie_list = movies["title"].values

    return render_template(
        "index.html",
        movies=movie_list,
        recommendations=recommended_movies
    )


if __name__ == "__main__":
    app.run(debug=True)