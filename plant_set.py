from datetime import datetime

import data_connection  # manages connection to server

add_set_query = 'AddPlantSet'

class PlantSet:
    def __init__(self):
        self.set_quantity = None
        self.plant_id = None
        self.my_season_id = None
        self.plot_id = None
        self.set_type_id = None

    def add_new_plant_set(self,
                          plant_id,
                          set_type_id,
                          set_quantity):
        self.plant_id = int(plant_id)
        self.set_quantity = int(set_quantity)
        self.set_type_id = int(set_type_id)

    def display_plant_set(self):
        print(self.__dict__)  # mostly for testing, DELETE before submission

    def add_plot_id(self,
                    plot_id):
        self.plot_id = int(plot_id)

    def add_season_id(self,
                      season_id):
        self.my_season_id = int(season_id)

    def export_plant_set(self,
                         set_quantity,
                         plant_id,
                         season_id,
                         plot_id,
                         set_type_id):
        self.set_quantity = int(set_quantity)
        self.plant_id = int(plant_id)
        self.season_id = int(season_id)
        self.plot_id = int(plot_id)
        self.set_type_id = int(set_type_id)

        print('hello')

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        # execute stored procedure to add new plant to database using inputs

        (cursor.execute
         (add_set_query + ' ?, ?, ?, ?, ?',
          [self.set_quantity,
           self.plant_id,
           self.season_id,
           self.plot_id,
           self.set_type_id]))

        cursor.commit()  # finalize entry into table

        print('Finished Inserting Plant ID number ' + str(self.plant_id))  # confirmation

        self.display_plant_set()

        this_connection.end_connection()
