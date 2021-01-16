import db_queries as myDB
import psycopg2 as dbapi2
import os

class Database:

    def addUser(self, username, password_hash):
        
        columns = "username, password_hash"
        username = username.replace("'","''")
        values = "'{}','{}'".format(username, password_hash)
        user_id = myDB.insertTable("user_table", columns, values, "user_id")
        return user_id


    def getUser(self, user_id):
        
        condition = "user_id = '{}'".format(user_id)
        selection = myDB.selectRows("user_table", condition)

        if selection is None or len(selection) == 0:
            return None

        userRow = selection[0]
        return userRow
       

    def getUserByUsername(self, username):

        username = username.replace("'","''")
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

        if len(columns) > 0 and columns[-1] == ',':
            columns = columns[:-1]

        if len(values) > 0 and values[-1] == ',':
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

        if len(settings) > 0 and settings[-1] == ',':
            settings = settings[:-1]

        myDB.updateRows("user_content", settings, condition)


    def addContent(self, title, content_type=None, type_specific_id=None):
        columns = "title,"
        title = title.replace("'","''")
        values = "'{}',".format(title)
        if content_type is not None and content_type != '':
            content_type = content_type.replace("'","''")
            columns += "content_type,"
            values += "'{}',".format(content_type)
        if type_specific_id is not None and type_specific_id != '':
            columns += "type_specific_id,"
            values += "'{}',".format(type_specific_id)

        if len(columns) > 0 and columns[-1] == ',':
            columns = columns[:-1]

        if len(values) > 0 and values[-1] == ',':
            values = values[:-1]

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
        title = title.replace("'","''")
        settings = "title = '{}'".format(title)

        myDB.updateRows("content", settings, condition)

    def addContentGenre(self, content_id, genre):
        columns = "content_id, genre"
        genre = genre.replace("'","''")
        values = "'{}','{}'".format(content_id, genre)
        myDB.insertTable("content_genre", columns, values)

    def getGenresFor(self, content_id):
        condition = "content_id = '{}'".format(content_id)
        selection = myDB.selectRows("content_genre", condition)

        if selection is None or len(selection) == 0:
            return None

        cgRow = selection
        return cgRow

    def deleteContentGenresFor(self, content_id):
        condition = "content_id = '{}'".format(content_id)
        myDB.deleteRows("content_genre", condition)

    def addBook(self, author=None, release_year=None, language=None, no_pages=None, isbn=None):
        columns = ""
        values = ""
        
        columns += "author,"
        if author is not None and author != '' and author != "None":
            author = author.replace("'", "''")
            values += "'{}',".format(author)
        else:
            values += "NULL,"
        
        columns += "release_year,"
        if release_year is not None and release_year != '':
            values += "'{}',".format(release_year)
        else:
            values += "NULL,"
        
        columns += "language,"
        if language is not None and language != '':
            language = language.replace("'", "''")
            values += "'{}',".format(language)
        else:
            values += "NULL,"
        
        columns += "no_pages,"
        if no_pages is not None and no_pages != '':
            values += "'{}',".format(no_pages)
        else:
            values += "NULL,"
        
        columns += "isbn"
        if isbn is not None and isbn != '':
            isbn = isbn.replace("'", "''")
            values += "'{}'".format(isbn)
        else:
            values += "NULL"

        book_id = myDB.insertTable("book", columns, values, "book_id")[0]
        return book_id
    

    def getBookInfosFor(self, user_id):
        columns = "content.content_id, book_id, title, author, release_year, language, no_pages, isbn, completion_status, owned, user_rating"

        joinPhrase = """
                     INNER JOIN content
                     ON user_content.content_id = content.content_id
                     INNER JOIN book
                     ON content.type_specific_id = book.book_id
                     """
        
        condition = "user_id = {} AND content.content_type = 'book'".format(user_id)

        return myDB.joinSelectRows("user_content", columns, joinPhrase, condition=condition)

    # unused
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
            author = author.replace("'", "''")
            settings += "author = '{}',".format(author)
        else:
            settings += "author = NULL,"

        if release_year is not None and release_year != "":
            settings += "release_year = '{}',".format(release_year)
        else:
            settings += "release_year = NULL,"
            
        if language is not None and language != "":
            language = language.replace("'", "''")
            settings += "language = '{}',".format(language)
        else:
            settings += "language = NULL,"
            
        if no_pages is not None and no_pages != "":
            settings += "no_pages = '{}',".format(no_pages)
        else:
            settings += "no_pages = NULL,"
            
        if isbn is not None and isbn != "":
            isbn = isbn.replace("'", "''")
            settings += "isbn = '{}'".format(isbn)
        else:
            settings += "isbn = NULL"

        myDB.updateRows("book", settings, condition)

    def addMovie(self, director=None, release_year=None, language=None, length=None, imdb_id=None):
        columns = ""
        values = ""
        
        columns += "director,"
        if director is not None and director != '' and director != "None":
            director = director.replace("'", "''")
            values += "'{}',".format(director)
        else:
            values += "NULL,"
        
        columns += "release_year,"
        if release_year is not None and release_year != '':
            values += "'{}',".format(release_year)
        else:
            values += "NULL,"
        
        columns += "language,"
        if language is not None and language != '':
            language = language.replace("'", "''")
            values += "'{}',".format(language)
        else:
            values += "NULL,"
        
        columns += "length,"
        if length is not None and length != '':
            values += "'{}',".format(length)
        else:
            values += "NULL,"
        
        columns += "imdb_id"
        if imdb_id is not None and imdb_id != '':
            imdb_id = imdb_id.replace("'", "''")
            values += "'{}'".format(imdb_id)
        else:
            values += "NULL"

        movie_id = myDB.insertTable("movie", columns, values, "movie_id")[0]
        return movie_id
    

    def getMovieInfosFor(self, user_id):
        columns = "content.content_id, movie_id, title, director, release_year, language, length, imdb_id, completion_status, owned, user_rating"

        joinPhrase = """
                     INNER JOIN content
                     ON user_content.content_id = content.content_id
                     INNER JOIN movie
                     ON content.type_specific_id = movie.movie_id
                     """
        
        condition = "user_id = {} AND content.content_type = 'movie'".format(user_id)

        return myDB.joinSelectRows("user_content", columns, joinPhrase, condition=condition)



    def deleteMovie(self, movie_id):
        condition = "movie_id = '{}'".format(movie_id)
        myDB.deleteRows("movie", condition)

    def updateMovie(self, movie_id, director=None, release_year=None, language=None, length=None, imdb_id=None):
        condition = "movie_id = '{}'".format(movie_id)
        settings = ""
            
        if director is not None and director != "":
            director = director.replace("'", "''")
            settings += "director = '{}',".format(director)
        else:
            settings += "author = NULL,"

        if release_year is not None and release_year != "":
            settings += "release_year = '{}',".format(release_year)
        else:
            settings += "release_year = NULL,"
            
        if language is not None and language != "":
            language = language.replace("'", "''")
            settings += "language = '{}',".format(language)
        else:
            settings += "language = NULL,"
            
        if length is not None and length != "":
            settings += "length = '{}',".format(length)
        else:
            settings += "length = NULL,"
            
        if imdb_id is not None and imdb_id != "":
            imdb_id = imdb_id.replace("'", "''")
            settings += "imdb_id = '{}'".format(imdb_id)
        else:
            settings += "imdb_id = NULL"

        myDB.updateRows("movie", settings, condition)

    def addSeries(self, release_year=None, language=None, no_seasons=None, imdb_id=None):
        columns = ""
        values = ""
        
        columns += "release_year,"
        if release_year is not None and release_year != '':
            values += "'{}',".format(release_year)
        else:
            values += "NULL,"
        
        columns += "language,"
        if language is not None and language != '':
            language = language.replace("'", "''")
            values += "'{}',".format(language)
        else:
            values += "NULL,"
        
        columns += "no_seasons,"
        if no_seasons is not None and no_seasons != '':
            values += "'{}',".format(no_seasons)
        else:
            values += "NULL,"
        
        columns += "imdb_id"
        if imdb_id is not None and imdb_id != '':
            imdb_id = imdb_id.replace("'", "''")
            values += "'{}'".format(imdb_id)
        else:
            values += "NULL"

        series_id = myDB.insertTable("series", columns, values, "series_id")[0]
        return series_id
    

    def getSeriesInfosFor(self, user_id):
        columns = "content.content_id, series_id, title, release_year, language, no_seasons, imdb_id, completion_status, owned, user_rating"

        joinPhrase = """
                     INNER JOIN content
                     ON user_content.content_id = content.content_id
                     INNER JOIN series
                     ON content.type_specific_id = series.series_id
                     """
        
        condition = "user_id = {} AND content.content_type = 'series'".format(user_id)

        return myDB.joinSelectRows("user_content", columns, joinPhrase, condition=condition)


    def deleteSeries(self, series_id):
        condition = "series_id = '{}'".format(series_id)
        myDB.deleteRows("series", condition)

    def updateSeries(self, series_id, release_year=None, language=None, no_seasons=None, imdb_id=None):
        condition = "series_id = '{}'".format(series_id)
        settings = ""

        if release_year is not None and release_year != "":
            settings += "release_year = '{}',".format(release_year)
        else:
            settings += "release_year = NULL,"
            
        if language is not None and language != "":
            language = language.replace("'", "''")
            settings += "language = '{}',".format(language)
        else:
            settings += "language = NULL,"
            
        if no_seasons is not None and no_seasons != "":
            settings += "no_seasons = '{}',".format(no_seasons)
        else:
            settings += "no_seasons = NULL,"
            
        if imdb_id is not None and imdb_id != "":
            imdb_id = imdb_id.replace("'", "''")
            settings += "imdb_id = '{}'".format(imdb_id)
        else:
            settings += "imdb_id = NULL"

        myDB.updateRows("series", settings, condition)

