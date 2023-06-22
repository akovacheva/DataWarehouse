import pyodbc


def get_connection(server_in, database_in):
    server = server_in
    database = database_in

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database}; Trusted_Connection=yes'
    connection = pyodbc.connect(connection_string)

    return connection



 