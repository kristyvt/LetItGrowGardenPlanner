"""
Connects to a SQL database using pyodbc
"""
import pyodbc


class Connection:
    def __init__(self):
        server = 'KRISTY-LAPTOP\\SQLEXPRESS'
        database = 'Garden'
        self.status = 'pending'

        try:

            connection_string = \
                (f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                 f'SERVER={server};'
                 f'DATABASE={database};'
                 f'trusted_connection=yes;'
                 f'Encrypt=No')

            self.connection = pyodbc.connect(connection_string)
            self.status = "success"

        except:
            print("no connection available")
            self.status = "failed"

    def end_connection(self):
        self.connection.close()


    def connect_to_master(self):
        try:

            connection_string = \
                (f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                 f'SERVER={'KRISTY-LAPTOP\\SQLEXPRESS'};'
                 f'DATABASE={'master'};'
                 f'trusted_connection=yes;'
                 f'Encrypt=No')

            self.connection = pyodbc.connect(connection_string)
            self.status = "success"

        except:
            print("no connection to master")
            self.status = "failed"
