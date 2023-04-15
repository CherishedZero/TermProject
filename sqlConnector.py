import mysql.connector
import getSQLLogin


def ExecuteAndCommit(query):
    with mysql.connector.connect(host='localhost', user=getSQLLogin.user, password=getSQLLogin.password,
                                 database='store') as mysql_connection:
        with mysql_connection.cursor() as mysql_cursor:
            mysql_cursor.execute(query)
            mysql_connection.commit()
            return mysql_cursor.rowcount


def ExecuteAndReturn(query):
    with mysql.connector.connect(host='localhost', user=getSQLLogin.user, password=getSQLLogin.password,
                                 database='store') as mysql_connection:
        with mysql_connection.cursor() as mysql_cursor:
            mysql_cursor.execute(query)
            return mysql_cursor.column_names, mysql_cursor.fetchall()
