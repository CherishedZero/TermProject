import mysql.connector


def execute_and_commit(query):
    print(query)
    with mysql.connector.connect(host='localhost', user='root', password='root',
                                 database='store') as mysql_connection:
        with mysql_connection.cursor() as mysql_cursor:
            mysql_cursor.execute(query)
            mysql_connection.commit()
            return mysql_cursor.rowcount


def execute_and_return(query):
    with mysql.connector.connect(host='localhost', user='root', password='root',
                                 database='store') as mysql_connection:
        with mysql_connection.cursor() as mysql_cursor:
            mysql_cursor.execute(query)
            return mysql_cursor.column_names, mysql_cursor.fetchall()