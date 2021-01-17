import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS user_table (
    user_id             SERIAL          NOT NULL,
    username            VARCHAR(100)    NOT NULL,
    password_hash       CHAR(64)        NOT NULL,
    creation_date       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    UNIQUE (username)
);
""",
"""
CREATE TABLE IF NOT EXISTS content (
	content_id          SERIAL          NOT NULL,
    content_type        VARCHAR(10),
    type_specific_id    INT,
    title               VARCHAR(100)    NOT NULL,
    PRIMARY KEY (content_id)
);
""",
"""
CREATE TABLE IF NOT EXISTS user_content (
    user_id             INT             NOT NULL,
    content_id          INT             NOT NULL,
    completion_status   BOOLEAN,
    owned               BOOLEAN,
    user_rating         INT,
    FOREIGN KEY (user_id) REFERENCES user_table(user_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id)
);
""",
"""
CREATE TABLE IF NOT EXISTS book (
    book_id             SERIAL             NOT NULL,
    author              VARCHAR(100),
    release_year        INT,
    language            VARCHAR(100),
    no_pages            INT,
    isbn                VARCHAR(100),
    PRIMARY KEY (book_id)
);
""",
"""
CREATE TABLE IF NOT EXISTS content_genre (
    content_id          INT             NOT NULL,
    genre               VARCHAR(100)    NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content(content_id)
);
""",
"""
CREATE TABLE IF NOT EXISTS movie (
    movie_id            SERIAL		NOT NULL,
    director            VARCHAR(100),
    release_year        INT,
    language            VARCHAR(100),
    length              INT,
    imdb_id             VARCHAR(100),
    PRIMARY KEY (movie_id)
);
""",
"""
CREATE TABLE IF NOT EXISTS series (
	series_id          	SERIAL		NOT NULL,
    release_year        INT,
    language            VARCHAR(100),
    no_seasons          INT,
    imdb_id             VARCHAR(100),
    PRIMARY KEY (series_id)
);
"""
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
            
            
        cursor.close()

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")

    if url is None:
        print("Usage: DATABASE_URL=url python db_init.py")
        sys.exit(1)
    initialize(url)
