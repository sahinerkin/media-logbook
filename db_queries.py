import os
import psycopg2 as dbapi2

def insertTable(table, column_list, value_list, returning=None):
    query = "INSERT INTO {}({}) values({})".format(table, column_list, value_list)
    if returning is None:
        # print(query)
        runQuery(query, returns=False)
    else:
        query += " RETURNING {}".format(returning)
        # print(query)
        queryResult = runQuery(query, returns=True)
        if queryResult is not None:
            # print(queryResult)
            return queryResult[0]


def selectRows(table, condition=None):
    query = "SELECT * FROM {}".format(table)
    
    if condition is not None:
        query += " WHERE {}".format(condition)
    
    return runQuery(query, returns=True)

def joinSelectRows(table, columns, joinPhrase, condition=None):
    query = "SELECT {} FROM {} ".format(columns, table)
    query += joinPhrase
    
    if condition is not None:
        query += " WHERE {}".format(condition)
    
    print(query)
    return runQuery(query, returns=True)


def deleteRows(table, condition):
    query = "DELETE FROM {} WHERE {}".format(table, condition)
    # print(query)
    runQuery(query, returns=False)

def updateRows(table, settings, condition):
    query = "UPDATE {} SET {} WHERE {}".format(table, settings, condition)
    # print(query)
    runQuery(query, returns=False)


def runQuery(query, returns = False):
    returnValue = None
    try:
        with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            if returns:
                returnValue = cursor.fetchall()
    except dbapi2.DatabaseError as dbError:
        if connection is not None:
            connection.rollback()
        returnValue = None
        print(dbError)
    finally:
        if connection is not None:
            connection.commit()
            connection.close()
        
        if cursor is not None:
            cursor.close()
        
        return returnValue