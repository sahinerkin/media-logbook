from flask import Flask, render_template, current_app, request, redirect, url_for, session
import db_queries as myDB
from hashlib import sha256
from datetime import datetime

def home(alert_message=None, alert_colour="danger"):
    
    db = current_app.config["db"]

    if 'user_id' in session:
        currentuser_id = session['user_id']
        user = db.getUser(currentuser_id)
        username = user[1]
        return redirect(url_for("books", username=username))

    return render_template("home.html", alert_message=alert_message, alert_colour=alert_colour)

def login():
    
    db = current_app.config["db"]

    if 'user_id' in session:
        currentuser_id = session['user_id']
        user = db.getUser(currentuser_id)
        username = user[1]
        return redirect(url_for("books", username=username))

    if request.method == "GET":
        return home()
    
    username = request.form.get("username")
    password = request.form.get("password")
    user_id = db.getUserByUsername(username)
    
    if user_id is not None:
        user = db.getUser(user_id)
        pw_bytestring = password.encode()
        password_hash = sha256(pw_bytestring).hexdigest() 
        if user[2] == password_hash:
            session['user_id'] = user_id
            return redirect(url_for("books", username=username))

    return home(alert_message="Couldn't log in. Please try again.")

def signup():
    
    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
        user = db.getUser(currentuser_id)
        username = user[1]
        return redirect(url_for("books", username=username))

    if request.method == "GET":
        return home()
    
    username = request.form.get("username_signup")
    password = request.form.get("password_signup")

    if username != "" and password != "" and db.getUserByUsername(username) is None:
        pw_bytestring = password.encode()
        password_hash = sha256(pw_bytestring).hexdigest()
        db.addUser(username, password_hash)
        return home(alert_message="Sign up successful!", alert_colour="success")

    return home(alert_message="Couldn't sign up. Please try again.")

def logout():
    session.pop('user_id', None)
    return home()

def test():
    return render_template("test.html")

def profile():
    if request.method == "GET":
        return

    page = request.form.get("page_name")
    username = request.form.get("user_profile")

    return redirect(url_for(page, username=username))


def books(username, rating_filter=None, completion_filter=None, owned_filter=None):
    db = current_app.config["db"]

    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    getUser = db.getUser
    user_id = db.getUserByUsername(username)
    getBookInfosFor = db.getBookInfosFor
    getGenresFor = db.getGenresFor
    if user_id:
        return render_template("book.html", user_id=user_id, currentuser_id = currentuser_id, rating_filter = rating_filter, completion_filter=completion_filter, owned_filter=owned_filter, getUser=getUser, getBookInfosFor=getBookInfosFor, getGenresFor=getGenresFor)
    
    return render_template("notfound.html", username=username)

def movies(username, rating_filter=None, completion_filter=None, owned_filter=None):
    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    getUser = db.getUser
    user_id = db.getUserByUsername(username)
    getMovieInfosFor = db.getMovieInfosFor
    getGenresFor = db.getGenresFor
    if user_id:
        return render_template("movie.html", user_id=user_id, currentuser_id = currentuser_id, rating_filter = rating_filter, completion_filter=completion_filter, owned_filter=owned_filter, getUser=getUser, getMovieInfosFor=getMovieInfosFor, getGenresFor=getGenresFor)
    
    return render_template("notfound.html", username=username)

def series(username, rating_filter=None, completion_filter=None, owned_filter=None):
    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    getUser = db.getUser
    user_id = db.getUserByUsername(username)
    getSeriesInfosFor = db.getSeriesInfosFor
    getGenresFor = db.getGenresFor
    if user_id:
        return render_template("series.html", user_id=user_id, currentuser_id = currentuser_id, rating_filter = rating_filter, completion_filter=completion_filter, owned_filter=owned_filter, getUser=getUser, getSeriesInfosFor=getSeriesInfosFor, getGenresFor=getGenresFor)
    
    return render_template("notfound.html", username=username)

def others(username, rating_filter=None, completion_filter=None, owned_filter=None):
    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    getUser = db.getUser
    user_id = db.getUserByUsername(username)
    getOtherInfosFor = db.getOtherInfosFor
    getGenresFor = db.getGenresFor
    if user_id:
        return render_template("other.html", user_id=user_id, currentuser_id = currentuser_id, rating_filter = rating_filter, completion_filter=completion_filter, owned_filter=owned_filter, getUser=getUser, getOtherInfosFor=getOtherInfosFor, getGenresFor=getGenresFor)
    
    return render_template("notfound.html", username=username)

def add_book(username):
    if request.method == "GET":
        return books(username)

    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    title = request.form.get("content_title").strip()

    if title == "":
        return books(username)

    author = request.form.get("author").strip()
    release_year = request.form.get("release_year")
    language = request.form.get("language").strip()
    no_pages = request.form.get("no_pages")
    isbn = request.form.get("isbn").strip()
    completed = request.form.get("completed")
    owned = request.form.get("owned")
    user_rating = request.form.get("user_rating")
    genresList = request.form.get("genres").split(',')


    user_id = db.getUserByUsername(username)
    if user_id != currentuser_id:
        return books(username)
    
    book_id = db.addBook(author=author, release_year=release_year, language=language, no_pages=no_pages, isbn=isbn)
    content_id = db.addContent(title, content_type="book", type_specific_id=book_id)
    db.addUserContent(user_id, content_id, completion_status=completed, owned=owned, user_rating=user_rating)

    for genreString in genresList:
        genre = genreString.strip()
        if genre != '':
            db.addContentGenre(content_id, genre)

    return redirect(url_for("books", username=username))

def add_movie(username):
    if request.method == "GET":
        return movies(username)

    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    title = request.form.get("content_title").strip()

    if title == "":
        return movies(username)

    director = request.form.get("director").strip()
    release_year = request.form.get("release_year")
    language = request.form.get("language").strip()
    length = request.form.get("length")
    imdb_id = request.form.get("imdb_id").strip()
    completed = request.form.get("completed")
    owned = request.form.get("owned")
    user_rating = request.form.get("user_rating")
    genresList = request.form.get("genres").split(',')


    user_id = db.getUserByUsername(username)
    if user_id != currentuser_id:
        return movies(username)
    
    movie_id = db.addMovie(director=director, release_year=release_year, language=language, length=length, imdb_id=imdb_id)
    content_id = db.addContent(title, content_type="movie", type_specific_id=movie_id)
    db.addUserContent(user_id, content_id, completion_status=completed, owned=owned, user_rating=user_rating)

    for genreString in genresList:
        genre = genreString.strip()
        if genre != '':
            db.addContentGenre(content_id, genre)

    return redirect(url_for("movies", username=username))


def add_series(username):
    if request.method == "GET":
        return series(username)

    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    title = request.form.get("content_title").strip()

    if title == "":
        return series(username)

    release_year = request.form.get("release_year")
    language = request.form.get("language").strip()
    no_seasons = request.form.get("no_seasons")
    imdb_id = request.form.get("imdb_id").strip()
    completed = request.form.get("completed")
    owned = request.form.get("owned")
    user_rating = request.form.get("user_rating")
    genresList = request.form.get("genres").split(',')


    user_id = db.getUserByUsername(username)
    if user_id != currentuser_id:
        return series(username)
    
    series_id = db.addSeries(release_year=release_year, language=language, no_seasons=no_seasons, imdb_id=imdb_id)
    content_id = db.addContent(title, content_type="series", type_specific_id=series_id)
    db.addUserContent(user_id, content_id, completion_status=completed, owned=owned, user_rating=user_rating)

    for genreString in genresList:
        genre = genreString.strip()
        if genre != '':
            db.addContentGenre(content_id, genre)

    return redirect(url_for("series", username=username))

def add_other(username):
    if request.method == "GET":
        return others(username)

    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    title = request.form.get("content_title").strip()

    if title == "":
        return others(username)

    completed = request.form.get("completed")
    owned = request.form.get("owned")
    user_rating = request.form.get("user_rating")
    genresList = request.form.get("genres").split(',')


    user_id = db.getUserByUsername(username)
    if user_id != currentuser_id:
        return others(username)
    
    content_id = db.addContent(title)
    db.addUserContent(user_id, content_id, completion_status=completed, owned=owned, user_rating=user_rating)

    for genreString in genresList:
        genre = genreString.strip()
        if genre != '':
            db.addContentGenre(content_id, genre)

    return redirect(url_for("others", username=username))


def delete():
    if request.method == "GET":
        return redirect(request.referrer)

    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    content_id = int(request.form.get("delete"))
    uc = db.getUserContent(currentuser_id, content_id)
    
    if uc is None:
        return redirect(request.referrer)


    content = db.getContent(content_id)
    content_type = content[1]

    db.deleteUserContent(currentuser_id, content_id)
    db.deleteContentGenresFor(content_id)
    db.deleteContent(content_id)
    
    if content_type == "book":
        book_id = content[2]
        db.deleteBook(book_id)  

    elif content_type == "movie":
        movie_id = content[2]
        db.deleteMovie(movie_id)

    elif content_type == "series":
        series_id = content[2]
        db.deleteSeries(series_id)

    return redirect(request.referrer)


def edit(content_id):
    if request.method == "GET":
        return redirect(request.referrer)

    db = current_app.config["db"]
    
    if 'user_id' in session:
        currentuser_id = session['user_id']
    else:
        currentuser_id = None

    uc = db.getUserContent(currentuser_id, content_id)
    
    if uc is None:
        return redirect(request.referrer)

    title = request.form.get("content_title").strip()
    

    if title == "":
        return redirect(request.referrer)


    db.deleteContentGenresFor(content_id)

    genresList = request.form.get("genres").split(',')

    for genreString in genresList:
        genre = genreString.strip()
        if genre != '':
            db.addContentGenre(content_id, genre)

    completed = request.form.get("completed")
    owned = request.form.get("owned")
    user_rating = request.form.get("user_rating")

    db.updateUserContent(currentuser_id, content_id, completion_status=completed, owned=owned, user_rating=user_rating)
    db.updateContent(content_id, title)

    content = db.getContent(content_id)
    content_type = content[1]


    if content_type == "book":
        author = request.form.get("author").strip()
        release_year = request.form.get("release_year")
        language = request.form.get("language").strip()
        no_pages = request.form.get("no_pages")
        isbn = request.form.get("isbn").strip()

        book_id = content[2]
        db.updateBook(book_id, author=author, release_year=release_year, language=language, no_pages=no_pages, isbn=isbn)

    elif content_type == "movie":
        director = request.form.get("director").strip()
        release_year = request.form.get("release_year")
        language = request.form.get("language").strip()
        length = request.form.get("length")
        imdb_id = request.form.get("imdb_id").strip()

        movie_id = content[2]
        db.updateMovie(movie_id, director=director, release_year=release_year, language=language, length=length, imdb_id=imdb_id)

    elif content_type == "series":
        release_year = request.form.get("release_year")
        language = request.form.get("language").strip()
        no_seasons = request.form.get("no_seasons")
        imdb_id = request.form.get("imdb_id").strip()

        series_id = content[2]
        db.updateSeries(series_id, release_year=release_year, language=language, no_seasons=no_seasons, imdb_id=imdb_id)

    return redirect(request.referrer)

