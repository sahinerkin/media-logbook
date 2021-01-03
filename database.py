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

    # unused
    def addUser(self, user):
        self._last_user_id += 1
        self.users[self._last_user_id] = user
        print("Added " + user.username)
        return self._last_user_id

    def deleteUser(self, user_id):
        if user_id in self.users:
            del self.users[user_id]

    def getUser(self, user_id):
        user = self.users.get(user_id)

        if user is None:
            return None

        user_ = User(user.username, user.password_hash, user.creation_date)
        return user_

    def getUserByUsername(self, username):

        for user_id, user in self.users.items():
            if user.username == username:
                return user_id
        
        return None

    # unused
    def getUsers(self):
        users = []
        for user_id, user in self.users.items():
            user_ = User(user.username, user.password_hash, user.creation_date)
            users.append({user_id, user_})
        return users


    def addUserContent(self, usercontent):
        self.usercontents.append(usercontent)

    # unused
    def deleteUserContent(self, user_id, content_id):
        usercontent = next((usercontent for usercontent in self.usercontents if usercontent.user_id == user_id and usercontent.content_id == content_id), None)
        del usercontent

    # unused
    def getUserContent(self, user_id, content_id):
        
        usercontent = next((usercontent for usercontent in self.usercontents if usercontent.user_id == user_id and usercontent.content_id == content_id), None)
        
        if usercontent is None:
            return None

        usercontent_ = UserContent(usercontent.user_id, usercontent.content_id, completion_status=usercontent.completion_status,
                                    owned=usercontent.owned, user_rating=usercontent.user_rating)
        return usercontent_

    
    def getUserContents(self):
        usercontents = []
        for usercontent in self.usercontents:
            usercontent_ = UserContent(usercontent.user_id, usercontent.content_id, completion_status=usercontent.completion_status,
                                    owned=usercontent.owned, user_rating=usercontent.user_rating)
            usercontents.append(usercontent_)
        return usercontents

    def addContent(self, content):
        self._last_content_id += 1
        self.contents[self._last_content_id] = content
        return self._last_content_id

    # unused
    def deleteContent(self, content_id):
        if content_id in self.contents:
            del self.contents[content_id]

    def getContent(self, content_id):
        content = self.contents.get(content_id)

        if content is None:
            return None

        content_ = Content(content.title, content_type=content.content_type, type_specific_id=content.type_specific_id)
        return content_

    # unused
    def getContents(self):
        contents = []
        for content_id, content in self.contents.items():
            content_ = Content(content.title, content_type=content.content_type, type_specific_id=content.type_specific_id)
            contents.append({content_id, content_})
        return contents

    # unused
    def getContentsOfTypes(self, content_types):
        contents = []
        for content_id, content in self.contents.items():
            if content.content_type in content_types:
                content_ = Content(content.title, content_type=content.content_type, type_specific_id=content.type_specific_id)
                contents.append({content_id, content_})
        return contents
    
    # unused
    def getContentsOtherThan(self, content_types):
        contents = []
        for content_id, content in self.contents.items():
            if content.content_type not in content_types:
                content_ = Content(content.title, content_type=content.content_type, type_specific_id=content.type_specific_id)
                contents.append({content_id, content_})
        return contents


    # def printContents(self):
    #     print("------------")
    #     print("Contents:")
    #     for i in range(self._last_content_id + 1):
    #         content = self.contents.get(i)
    #         if (content is not None):
    #             print(content.title)

    #     print("------------\n")

    def addBook(self, book):
        self._last_book_id += 1
        self.books[self._last_book_id] = book
        return self._last_book_id

    # unused
    def deleteBook(self, book_id):
        if book_id in self.books:
            del self.books[book_id]

    def getBook(self, book_id):
        book = self.books.get(book_id)

        if book is None:
            return None

        book_ = Book(author=book.author, release_year=book.release_year, language=book.language, no_pages=book.no_pages, isbn=book.isbn)
        return book_

    def getBooks(self):
        books = []
        for book_id, book in self.books.items():
            book_ = Book(author=book.author, release_year=book.release_year, language=book.language, no_pages=book.no_pages, isbn=book.isbn)
            books.append({book_id, book_})
        return books


