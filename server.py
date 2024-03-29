from flask import Flask, session
import view
import os
from db_init import initialize
from psycopg2 import extensions
from database import Database

onHeroku = True

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ZGCiPZ5cygTxcxv1PMn1j4VCWowpNGHg'

    app.add_url_rule("/", view_func=view.home)
    app.add_url_rule("/", methods=["GET", "POST"], view_func=view.signup)
    app.add_url_rule("/login", methods=["GET", "POST"], view_func=view.login)
    app.add_url_rule("/logout", methods=["GET"], view_func=view.logout)
    app.add_url_rule("/profile", methods=["GET", "POST"], view_func=view.profile)
    app.add_url_rule("/test", view_func=view.test)
    app.add_url_rule("/<string:username>/books", view_func=view.books)
    app.add_url_rule("/<string:username>/books/rating/<int:rating_filter>", view_func=view.books)
    app.add_url_rule("/<string:username>/books/owned/<string:owned_filter>", view_func=view.books)
    app.add_url_rule("/<string:username>/books/completed/<string:completion_filter>", view_func=view.books)

    app.add_url_rule("/<string:username>/movies", view_func=view.movies)
    app.add_url_rule("/<string:username>/movies/rating/<int:rating_filter>", view_func=view.movies)
    app.add_url_rule("/<string:username>/movies/owned/<string:owned_filter>", view_func=view.movies)
    app.add_url_rule("/<string:username>/movies/completed/<string:completion_filter>", view_func=view.movies)

    app.add_url_rule("/<string:username>/series", view_func=view.series)
    app.add_url_rule("/<string:username>/series/rating/<int:rating_filter>", view_func=view.series)
    app.add_url_rule("/<string:username>/series/owned/<string:owned_filter>", view_func=view.series)
    app.add_url_rule("/<string:username>/series/completed/<string:completion_filter>", view_func=view.series)

    app.add_url_rule("/<string:username>/others", view_func=view.others)
    app.add_url_rule("/<string:username>/others/rating/<int:rating_filter>", view_func=view.others)
    app.add_url_rule("/<string:username>/others/owned/<string:owned_filter>", view_func=view.others)
    app.add_url_rule("/<string:username>/others/completed/<string:completion_filter>", view_func=view.others)

    app.add_url_rule("/<string:username>/books", methods=["GET", "POST"], view_func=view.add_book)
    app.add_url_rule("/<string:username>/movies", methods=["GET", "POST"], view_func=view.add_movie)
    app.add_url_rule("/<string:username>/series", methods=["GET", "POST"], view_func=view.add_series)
    app.add_url_rule("/<string:username>/others", methods=["GET", "POST"], view_func=view.add_other)
    
    app.add_url_rule("/delete", methods=["POST"], view_func=view.delete)
    app.add_url_rule("/edit/<int:content_id>", methods=["POST"], view_func=view.edit)

    extensions.register_type(extensions.UNICODE)
    extensions.register_type(extensions.UNICODEARRAY)    

    if not onHeroku:
        os.environ["DATABASE_URL"] = "dbname='postgres' user='postgres' host='localhost' password='*26pg05#'"
        initialize(os.environ.get("DATABASE_URL"))

    db = Database()

    app.config["db"] = db
    return app

app = create_app()

if __name__ == "__main__":
    if not onHeroku:
        app.run(host="0.0.0.0", port=8080, debug=True)
    else:
        app.run(host="0.0.0.0", port=8080, debug=False)