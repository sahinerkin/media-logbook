import db_queries as myDB
import psycopg2 as dbapi2
import os
from user import User
from usercontent import UserContent
from content import Content
from book import Book

class Database:
    def __init__(self):
        self.users = {}
        self.usercontents = []
        self.contents = {}
        self.books = {}
        self._last_user_id = 0
        self._last_content_id = 0
        self._last_book_id = 0

    def addUser(self, username, password_hash):
        
        columns = "username, password_hash"
        values = "'{}','{}'".format(username, password_hash)
        user_id = myDB.insertTable("user_table", columns, values, "user_id")
        return user_id


    def getUser(self, user_id):
        
        condition = "user_id = '{}'".format(user_id)
        selection = myDB.selectRows("user_table", condition)

        if selection is None or len(selection) == 0:
            return None

        userRow = selection[0]
        # user_ = User(userRow[0], userRow[1], userRow[2])
        return userRow
       

    def getUserByUsername(self, username):

        condition = "username = '{}'".format(username)
        selection = myDB.selectRows("user_table", condition)
        if selection is None or len(selection) == 0:
            return None

        userRow = selection[0][0]
        return userRow


    def addUserContent(self, user_id, content_id, completion_status=None, owned=None, user_rating=None):
        columns = "user_id,content_id,"
        values = "'{}','{}',".format(user_id, content_id)

        columns += "completion_status,"
        if completion_status == "on":
            values += "'true',"
        else:
            values += "'false',"

        columns += "owned,"
        if owned == "on":
            values += "'true',"
        else:
            values += "'false',"

        if user_rating is not None:
            columns += "user_rating,"
            values += "'{}',".format(user_rating)

        if columns[-1] == ',':
            columns = columns[:-1]

        if values[-1] == ',':
            values = values[:-1]

        myDB.insertTable("user_content", columns, values, "user_id")

    def getUserContent(self, user_id, content_id):
        condition = "user_id = '{}' AND content_id = '{}'".format(user_id, content_id)
        selection = myDB.selectRows("user_content", condition)

        if selection is None or len(selection) == 0:
            return None

        ucRow = selection[0]
        return ucRow

    def getUserContents(self):
        selection = myDB.selectRows("user_content")

        if selection is None or len(selection) == 0:
            return None

        return selection

    def deleteUserContent(self, user_id, content_id):
        condition = "user_id = '{}' AND content_id = '{}'".format(user_id, content_id)
        myDB.deleteRows("user_content", condition)

    def updateUserContent(self, user_id, content_id, completion_status=None, owned=None, user_rating=None):
        condition = "user_id = '{}' AND content_id = '{}'".format(user_id, content_id)
        settings = ""

        if completion_status == "on":
            settings += "completion_status = true,"
        else:
            settings += "completion_status = false,"
        
        if owned == "on":
            settings += "owned = true,"
        else:
            settings += "owned = false,"
            
        if user_rating is not None and user_rating != "":
            settings += "user_rating = '{}',".format(user_rating)

        if settings[-1] == ',':
            settings = settings[:-1]

        myDB.updateRows("user_content", settings, condition)


    def addContent(self, title, content_type=None, type_specific_id=None):
        columns = "title,"
        values = "'{}',".format(title)
        if content_type is not None and content_type != '':
            columns += "content_type,"
            values += "'{}',".format(content_type)
        if type_specific_id is not None and type_specific_id != '':
            columns += "type_specific_id,"
            values += "'{}',".format(type_specific_id)

        if columns[-1] == ',':
            columns = columns[:-1]

        if values[-1] == ',':
            values = values[:-1]

        print("Add content query!!!")
        content_id = myDB.insertTable("content", columns, values, "content_id")[0]
        return content_id


    def getContent(self, content_id):

        condition = "content_id = '{}'".format(content_id)
        selection = myDB.selectRows("content", condition)

        if selection is None or len(selection) == 0:
            return None

        contentRow = selection[0]
        return contentRow



    def deleteContent(self, content_id):
        condition = "content_id = '{}'".format(content_id)
        myDB.deleteRows("content", condition)

    def updateContent(self, content_id, title):
        condition = "content_id = '{}'".format(content_id)
        settings = "title = '{}'".format(title)

        myDB.updateRows("content", settings, condition)


    def addBook(self, author=None, release_year=None, language=None, no_pages=None, isbn=None):
        columns = ""
        values = ""
        if author is not None and author != '':
            columns += "author,"
            values += "'{}',".format(author)
        if release_year is not None and release_year != '':
            columns += "release_year,"
            values += "'{}',".format(release_year)
        if language is not None and language != '':
            columns += "language,"
            values += "'{}',".format(language)
        if no_pages is not None and no_pages != '':
            columns += "no_pages,"
            values += "'{}',".format(no_pages)
        if isbn is not None and isbn != '':
            columns += "isbn,"
            values += "'{}',".format(isbn)

        if columns[-1] == ',':
            columns = columns[:-1]

        if values[-1] == ',':
            values = values[:-1]

        print("Add book query!!!")
        book_id = myDB.insertTable("book", columns, values, "book_id")[0]
        return book_id

    def getBook(self, book_id):
        condition = "book_id = '{}'".format(book_id)
        selection = myDB.selectRows("book", condition)

        if selection is None or len(selection) == 0:
            return None

        bookRow = selection[0]
        return bookRow

    def deleteBook(self, book_id):
        condition = "book_id = '{}'".format(book_id)
        myDB.deleteRows("book", condition)

    def updateBook(self, book_id, author=None, release_year=None, language=None, no_pages=None, isbn=None):
        condition = "book_id = '{}'".format(book_id)
        settings = ""
            
        if author is not None and author != "":
            settings += "author = '{}',".format(author)

        if release_year is not None and release_year != "":
            settings += "release_year = '{}',".format(release_year)

        if language is not None and language != "":
            settings += "language = '{}',".format(language)

        if no_pages is not None and no_pages != "":
            settings += "no_pages = '{}',".format(no_pages)

        if isbn is not None and isbn != "":
            settings += "isbn = '{}',".format(isbn)

        if settings[-1] == ',':
            settings = settings[:-1]

        myDB.updateRows("book", settings, condition)
