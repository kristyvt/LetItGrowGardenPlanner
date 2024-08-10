'''
Let it Grow Garden Planner
Garden planning and outcome tracking tool
Kristy Stark
Champlain College SDEV-435-81

export_query exports data retrieved from SQL to CSV
Last Revised 8/3/24
'''

import csv
import data_connection
import os

outcome_detail_query = 'QueryOutcomeDetail'


class ExportQuery:
    def __init__(self):
        self.header = []

    def export_csv(self, query_name, header):
        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        download_path = os.path.expanduser("~") + '\\Downloads\\' + query_name + '.csv'

        cursor.execute(query_name)

        data = cursor.fetchall()

        with open(download_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)

        return download_path

