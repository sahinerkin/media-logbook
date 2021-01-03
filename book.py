class Book:
    def __init__(self, author=None, release_year=None, language=None, no_pages=None, isbn=None):
        self.author = author
        self.release_year = release_year
        self.language = language
        self.no_pages = no_pages
        self.isbn = isbn