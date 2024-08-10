'''
Let it Grow Garden Planner
Garden planning and outcome tracking tool
Kristy Stark
Champlain College SDEV-435-81

plant_set manages specific planting occurrence details
Last Revised 8/3/24
'''

import data_connection  # manages connection to server

add_set_query = 'AddPlantSet'
plant_set_query = 'QueryPlantSetData'
update_set_query = 'UpdatePlantSet'


# Manages planting occurrence details using a Plantset object
class PlantSet:
    def __init__(self):
        self.set_quantity = None
        self.plant_id = None
        self.my_season_id = None
        self.plot_id = None
        self.set_type_id = None

    # set values that apply to all plant sets
    def add_new_plant_set(self,
                          plant_id,
                          set_type_id,
                          set_quantity):
        self.plant_id = int(plant_id)
        self.set_quantity = int(set_quantity)
        self.set_type_id = int(set_type_id)

    # used for testing
    def display_plant_set(self):
        print(self.__dict__)

    # Function to assign a plot ID to a plant set
    def add_plot_id(self,
                    plot_id):
        self.plot_id = int(plot_id)

    # Function to assign a season ID to a plant set
    def add_season_id(self,
                      season_id):
        self.my_season_id = int(season_id)

    # Function to export new plant set data to SQL database
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

        self.display_plant_set()

        this_connection.end_connection()

    # Function to import plant set details to display onscreen
    def import_plant_set(self,
                         plant_selection,
                         season_selection,
                         q_plant_set_id):

        self.plant_name = plant_selection
        self.season_text = season_selection

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

            if self.plant_set_id is None:
                print('not found')

            else:
                self.plant_set_id = r[0]
                print(r)
                print(r[0])
                break

        return self.plant_set_id

    # Function to export edited set details to SQL

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
        self.plant_set_notes = plant_set_notes

        if outcome is None:
            self.outcome = None
        else:
            self.outcome = bool(outcome)

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

        this_connection.end_connection()
