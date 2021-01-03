from flask import Flask, render_template, current_app, request, redirect, url_for
from hashlib import sha256
from datetime import datetime
from user import User
from usercontent import UserContent
from content import Content
from book import Book

def home():
    
    db = current_app.config["db"]
    currentuser_id = current_app.config["currentuser"]
    

    if currentuser_id is not None:
        user = db.getUser(currentuser_id)
        username = user.username
        return redirect(url_for("books", username=username))

    return render_template("home.html")

def login():
    
    db = current_app.config["db"]
    currentuser_id = current_app.config["currentuser"]
    

    if currentuser_id is not None:
        user = db.getUser(currentuser_id)
        username = user.username
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
        if user.password_hash == password_hash:
            current_app.config["currentuser"] = user_id
            return redirect(url_for("books", username=username))

    return home()

def signup():
    
    db = current_app.config["db"]
    currentuser_id = current_app.config["currentuser"]
    
    if currentuser_id is not None:
        user = db.getUser(currentuser_id)
        username = user.username
        return redirect(url_for("books", username=username))

    if request.method == "GET":
        return home()
    
    username = request.form.get("username_signup")
    password = request.form.get("password_signup")

    if username != "" and password != "" and db.getUserByUsername(username) is None:
        pw_bytestring = password.encode()
        password_hash = sha256(pw_bytestring).hexdigest()
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.addUser(User(username, password_hash, creation_date))

    return home()

def logout():
    current_app.config["currentuser"] = None
    print(current_app.config["currentuser"])
    return home()

def test():
    return render_template("test.html")

def books(username):
    db = current_app.config["db"]
    currentuser_id = current_app.config["currentuser"]
    getUser = db.getUser
    user_id = db.getUserByUsername(username)
    usercontents = db.getUserContents()
    getContent = db.getContent
    getBook = db.getBook
    return render_template("book.html", user_id=user_id, currentuser_id = currentuser_id, getUser=getUser, usercontents=usercontents, getContent=getContent, getBook=getBook)

def add_book(username):
    if request.method == "GET":
        return books(username)

    db = current_app.config["db"]

    title = request.form.get("book_title").strip()

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

    user_id = db.getUserByUsername(username)
    book = Book(author, release_year=release_year, language=language, no_pages=no_pages, isbn=isbn)
    book_id = db.addBook(book)
    content = Content(title, content_type="book", type_specific_id=book_id)
    content_id = db.addContent(content)
    db.addUserContent(UserContent(user_id, content_id, completion_status=completed, owned=owned, user_rating=user_rating))

    print(owned)
    print(completed)
    
    return redirect(url_for("books", username=username))

def delete():
    if request.method == "GET":
        return home()

    db = current_app.config["db"]
    currentuser_id = current_app.config["currentuser"]

    content_id = int(request.form.get("delete"))
    uc = db.getUserContent(currentuser_id, content_id)
    
    if uc is None:
        return home()

    # GENERALIZE THE FUNCTION FOR ALL TYPES OF CONTENT
    # WITH IF BLOCK (CONTENT_TYPE)

    content = db.getContent(content_id)
    book_id = content.type_specific_id

    db.deleteUserContent(currentuser_id, content_id)
    db.deleteContent(content_id)
    db.deleteBook(book_id)

    return home()

def edit(content_id):
    if request.method == "GET":
        return home()

    print("Editing: " + str(content_id))
    print(type(content_id))

    """ db = current_app.config["db"]
    currentuser_id = current_app.config["currentuser"]

    content_id = int(request.form.get("delete"))
    uc = db.getUserContent(currentuser_id, content_id)
    
    if uc is None:
        return home()

    # GENERALIZE THE FUNCTION FOR ALL TYPES OF CONTENT
    # WITH IF BLOCK (CONTENT_TYPE)

    content = db.getContent(content_id)
    book_id = content.type_specific_id

    db.deleteUserContent(currentuser_id, content_id)
    db.deleteContent(content_id)
    db.deleteBook(book_id) """

    return home()