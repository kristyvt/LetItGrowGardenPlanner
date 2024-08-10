'''
Let it Grow Garden Planner
Garden planning and outcome tracking tool
Kristy Stark
Champlain College SDEV-435-81

data_connection manages connection to a SQL database using pyodbc
Last Revised 8/3/24
'''

import pyodbc   # needs to be installed if not already present

class Connection:

    # Create new connection object
    # Set database details
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
            self.status = "failed"

    # Function to close the SQL connection
    def end_connection(self):
        self.connection.close()

    # Function to connect to the master database
    # Used to check if the Garden database is present at startup
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
            self.status = "failed"
