import mysql.connector
import getSQLLogin


def ExecuteAndCommit(query):
    """
        Executes a query on the specified database and commits the changes.

        Args:
        - query (str): the SQL query to execute.
        - host (str): the hostname of the MySQL server.
        - username (str): the username to connect to the MySQL server.
        - password (str): the password to connect to the MySQL server.
        - port (int): the port number of the MySQL server.
        - database (str): The name of the database to use.

        Returns:
        An integer value representing the number of affected rows after executing the query.
    """
    with mysql.connector.connect(host='localhost', user=getSQLLogin.user, password=getSQLLogin.password,
                                 database='store') as mysql_connection:
        with mysql_connection.cursor() as mysql_cursor:
            mysql_cursor.execute(query)
            mysql_connection.commit()
            return mysql_cursor.rowcount


def ExecuteAndReturn(query):
    """
        Executes a SQL query and returns the result set.

        Args:
        - query (str): The SQL query to execute.
        - host (str): The hostname of the MySQL server.
        - username (str): The username to connect to the MySQL server.
        - password (str): The password to connect to the MySQL server.
        - port (int): The port number of the MySQL server.
        - database (str): The name of the database to use.

        Returns:
        A tuple containing two elements:
        - A list of strings representing the column names of the result set.
        - A list of tuples, where each tuple contains the values of a single row in the result set.

        If the query doesn't return any rows, the second element of the tuple will be an empty list.
        If an error occurs during the execution of the query, an exception will be raised.
    """
    with mysql.connector.connect(host='localhost', user=getSQLLogin.user, password=getSQLLogin.password,
                                 database='store') as mysql_connection:
        with mysql_connection.cursor() as mysql_cursor:
            mysql_cursor.execute(query)
            return mysql_cursor.column_names, mysql_cursor.fetchall()