'''
Let it Grow Garden Planner
Garden planning and outcome tracking tool
Kristy Stark
Champlain College SDEV-435-81

my_season is used to create new seasons and retrieve season details
Last Revised 8/3/24
'''

import data_connection  # manages connection to server

add_season_query = 'AddSeason'
my_season_query = 'QueryMySeasonData'
update_season_query = 'UpdateMySeason'  # to be created


# class to manage details regarding a specific season
class MySeason:
    def __init__(self):
        self.my_season_id = None
        self.season_text = None
        self.season_year = None
        self.spring = None
        self.fall = None

    # Season is Spring or Fall
    # Set season text value automatically based on
    # season name and year passed from calling func.
    def set_season_values(self, season, year):
        self.season_year = year
        year_text = str(year)
        self.season_text = (season
                            + str(year_text[2])
                            + str(year_text[3]))
        if season == 'Spring':
            self.spring = True
        else:
            self.spring = False
        if season == 'Fall':
            self.fall = True
        else:
            self.fall = False

    # Export new season entry to SQL database
    def export_season(self):
        self.new_season_text = str(self.season_text)
        self.new_season_year = int(self.season_year)

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        (cursor.execute
         (add_season_query + ' ?, ?, ?, ?',
          [self.new_season_text,
           self.new_season_year,
           self.spring,
           self.fall]))

        cursor.commit()  # finalize entry into table

        this_connection.end_connection()

        # return text for use with confirmation message

        return self.new_season_text

    # Function to import season details to display onscreen
    def import_my_season(self, my_season_id):

        self.season_text = None
        self.season_year = None
        self.spring = None
        self.fall = None
        self.season_active = None

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(my_season_query + ' ?',
                       [my_season_id])

        records = cursor.fetchall()
        for r in records:
            self.my_season_id = r[0]
            self.my_season_text = r[1]
            self.my_season_year = r[2]
            self.spring = r[3]
            self.fall = r[4]
            self.season_active = r[5]

            if self.my_season_id is None:
                print('not found')

            else:
                self.my_season_id = r[0]
                break

        return self.my_season_id

    def display_season(self):
        print(self.__dict__)  # available for testing purposes