from flask import Flask
import view
from database import Database
from user import User
from usercontent import UserContent
from content import Content
from book import Book

def create_app():
    app = Flask(__name__)
    app.add_url_rule("/", view_func=view.home)
    app.add_url_rule("/", methods=["GET", "POST"], view_func=view.signup)
    app.add_url_rule("/login", methods=["GET", "POST"], view_func=view.login)
    app.add_url_rule("/logout", methods=["GET"], view_func=view.logout)
    app.add_url_rule("/test", view_func=view.test)
    app.add_url_rule("/<string:username>/books", view_func=view.books)
    app.add_url_rule("/<string:username>/books", methods=["GET", "POST"], view_func=view.add_book)
    app.add_url_rule("/delete", methods=["POST"], view_func=view.delete)
    app.add_url_rule("/edit/<int:content_id>", methods=["POST"], view_func=view.edit)
    app.config.from_object("settings")

    db = Database()
    db.addUser(User("sahnerkin", "8d85f559ec1a56d9e6d80b72f61c22b9bd4939034cdaf88e8e7a13868f24c73e", "123"))
    
    db.addUserContent(UserContent(1, 1, completion_status=True, owned=True, user_rating=4))
    db.addUserContent(UserContent(1, 4, completion_status=False, owned=False, user_rating=1))

    db.addContent(Content("1984", content_type="book", type_specific_id=1))
    db.addBook(Book(author="George Orwell", language="English", no_pages=300))

    db.addContent(Content("Tenet", content_type="movies", type_specific_id=1))

    db.addContent(Content("B99", content_type="series", type_specific_id=1))

    db.addContent(Content("Bir Bilim Adamının Romanı", content_type="book", type_specific_id=2))
    db.addBook(Book(author="Oğuz Atay", language="Turkish", no_pages=260))
    
    app.config["db"] = db
    app.config["currentuser"] = None
    return app



if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, )