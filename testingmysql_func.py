import mysql.connector


def executeQueryAndReturnResult(query, host='localhost', username='root', password='root', port=3306,
                                database='store'):
    """
        Executes a SQL query and returns the result set.

        Args:
        - query (str): The SQL query to execute.
        - host (str): The hostname of the MySQL server. (Default is 'localhost'.)
        - username (str): The username to connect to the MySQL server. (Default is 'root'.)
        - password (str): The password to connect to the MySQL server. (Default is 'root'.)
        - port (int): The port number of the MySQL server. (Default is 3306.)
        - database (str): The name of the database to use. (Default is 'doctor_management_system'.)

        Returns:
        A tuple containing two elements:
        - A list of strings representing the column names of the result set.
        - A list of tuples, where each tuple contains the values of a single row in the result set.

        If the query doesn't return any rows, the second element of the tuple will be an empty list.
        If an error occurs during the execution of the query, an exception will be raised.
        """
    with mysql.connector.connect(host=host, user=username, password=password, port=port, database=database) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result_set = cursor.fetchall()
            if result_set is not None:
                return cursor.column_names, result_set
            else:
                return None, []


def executeQueryAndCommit(query, host='localhost', username='root', password='root', port=3306, database='store'):
    """
        Executes a query on the specified database and commits the changes.

        Args:
        - query (str): the SQL query to execute.
        - host (str): the hostname of the MySQL server (Default is 'localhost').
        - username (str): the username to connect to the MySQL server (Default is 'root').
        - password (str): the password to connect to the MySQL server (Default is 'root').
        - port (int): the port number of the MySQL server (default is 3306).
        - database (str): The name of the database to use. (Default is 'doctor_management_system'.)

        Returns:
        An integer value representing the number of affected rows after executing the query.
        """
    with mysql.connector.connect(host=host, user=username, password=password, port=port, database=database) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(query)
            except Exception as e:
                print(e)
            conn.commit()
            row_count = cursor.rowcount
            if row_count is not None:
                return row_count
            else:
                return 0