"""
Connects to a SQL database using pyodbc
"""
import pyodbc


class Connection:
    def __init__(self):
        server = 'KRISTY-LAPTOP\\SQLEXPRESS'
        database = 'Garden'

        connection_string = \
            (f'DRIVER={{ODBC Driver 18 for SQL Server}};'
             f'SERVER={server};'
             f'DATABASE={database};'
             f'trusted_connection=yes;'
             f'Encrypt=No')

        self.connection = pyodbc.connect(connection_string)

    def end_connection(self):
        self.connection.close()
