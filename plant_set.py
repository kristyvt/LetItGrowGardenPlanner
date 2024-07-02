from datetime import datetime

import data_connection  # manages connection to server

add_set_query = 'AddPlantSet'
plant_set_query = 'QueryPlantSetData'
update_set_query = 'UpdatePlantSet'


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

    def import_plant_set(self,
                         plant_selection,
                         season_selection):

        q_plant_set_id = 0

        self.plant_name = plant_selection
        self.season_text = season_selection

        print(self.plant_name)

        self.set_quantity = None
        self.plant_id = None
        self.my_season_id = None
        self.plot_id = None
        self.set_type = None
        self.planted_date = None
        self.first_harvest_date = None
        self.last_harvest_date = None
        self.outcome = None
        self.plant_set_notes = None
        self.plant_set_id = None

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(plant_set_query + ' ?, ?, ?',
                       [plant_selection,
                        season_selection,
                        q_plant_set_id])

        records = cursor.fetchall()
        for r in records:
            self.plant_set_id = r[0]
            q_plant_name = r[1]
            q_plant_season_text = r[2]
            self.plot_id = r[3]
            self.set_type = r[4]
            self.set_quantity = r[5]
            self.planted_date = r[6]
            self.first_harvest_date = r[7]
            self.last_harvest_date = r[8]
            self.outcome = r[9]
            self.plant_set_notes = r[10]

            print('test')

            if self.plant_set_id is None:
                print('not found')

            else:
                self.plant_set_id = r[0]
                print(r)
                print(r[0])
                break

        return self.plant_set_id

    def export_updated_set(self,
                           plant_set_id,
                           set_quantity,
                           planted_date,
                           first_harvest_date,
                           last_harvest_date,
                           outcome,
                           plant_id,
                           season_id,
                           plot_id,
                           set_type_id,
                           plant_set_notes):
        self.plant_set_id = plant_set_id
        self.set_quantity = int(set_quantity)
        self.plant_id = int(plant_id)
        self.season_id = int(season_id)
        self.plot_id = int(plot_id)
        self.set_type_id = int(set_type_id)
        self.planted_date = planted_date
        self.first_harvest_date = first_harvest_date
        self.last_harvest_date = last_harvest_date
        self.outcome = bool(outcome)
        self.plant_set_notes = plant_set_notes

        print('hello')

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        # execute stored procedure to add new plant to database using inputs

        (cursor.execute
         (update_set_query + ' ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?',
          [self.plant_set_id,
           self.set_quantity,
           self.planted_date,
           self.first_harvest_date,
           self.last_harvest_date,
           self.outcome,
           self.plant_id,
           self.season_id,
           self.plot_id,
           self.set_type_id,
           self.plant_set_notes]))

        cursor.commit()  # finalize entry into table

        print('Finished Inserting Plant Set ID number ' + str(self.plant_set_id))  # confirmation

        self.display_plant_set()

        this_connection.end_connection()
