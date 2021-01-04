import os
import psycopg2 as dbapi2

def insertTable(table, column_list, value_list, returning=None):
    query = "INSERT INTO {}({}) values({})".format(table, column_list, value_list)
    if returning is None:
        print(query)
        runQuery(query)
    else:
        query += " RETURNING {}".format(returning)
        print(query)
        queryResult = runQuery(query)
        if queryResult is not None:
            print(queryResult)
            return queryResult[0]


def selectRows(table, condition=None):
    query = "SELECT * FROM {}".format(table)
    
    if condition is not None:
        query += " WHERE {}".format(condition)
    
    return runQuery(query)


def deleteRows(table, condition):
    query = "DELETE FROM {} WHERE {}".format(table, condition)
    print(query)
    runQuery(query)

def updateRows(table, settings, condition):
    query = "UPDATE {} SET {} WHERE {}".format(table, settings, condition)
    print(query)
    runQuery(query)


def runQuery(query, keywords=[]):
    returnValue = None
    try:
        with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            if "INSERT" in query or "SELECT" in query:
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
        
        if keywords != []:
            finalResult = list([result for result in returnValue])
            resultDicts = []
            for row in finalResult:

                myDict = {}
                for i, keyword in enumerate(keywords):
                    myDict[keyword] = row[i]
                
                resultDicts.append(myDict)
            
            if len(resultDicts) == 1:
                return resultDicts[0]

            return resultDicts
        return returnValue