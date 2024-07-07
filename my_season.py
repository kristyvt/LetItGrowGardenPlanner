import data_connection  # manages connection to server

add_season_query = 'AddSeason'
my_season_query = 'QueryMySeasonData'
update_season_query = 'UpdateMySeason'  # to be created

# next steps
# decide how to handle changing of seasons...
        # on edit page or separate button?
        # if on edit, need to include functionality to update plot nitrogen levels


class MySeason:
    def __init__(self):
        self.my_season_id = None
        self.season_text = None
        self.season_year = None
        self.spring = None
        self.fall = None

    # season is Spring or Fall - set up as checkbox
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

        print(self.season_text)
        print(self.spring)
        print(self.fall)


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

        print('Finished Inserting Season '
              + self.new_season_text)  # confirmation

        this_connection.end_connection()

        return self.new_season_text


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
                print(r)
                print(r[0])
                break

        return self.my_season_id


    def export_updated_season(self,
                              my_season_id,
                              my_season_text,
                              my_season_year,
                              spring,
                              fall,
                              season_active):

        self.season_id = int(my_season_id)
        self.season_text = str(my_season_text)
        self.season_year = int(my_season_year)
        self.spring = bool(spring)
        self.fall = bool(fall)
        self.season_active = bool(season_active)

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        # execute stored procedure to add new plant to database using inputs

        (cursor.execute
         (update_season_query + ' ?, ?, ?, ?, ?, ?',
          [self.season_id,
           self.season_text,
           self.season_year,
           self.spring,
           self.fall,
           self.season_active]))

        cursor.commit()  # finalize entry into table

        print('Finished Inserting Season: '
              + str(self.season_text))  # confirmation

        self.display_season()

        this_connection.end_connection()

    def display_season(self):
        print(self.__dict__)  # mostly for testing, DELETE before submission