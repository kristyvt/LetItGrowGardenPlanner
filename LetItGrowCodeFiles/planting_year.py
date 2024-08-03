'''
Let it Grow Garden Planner
Garden planning and outcome tracking tool
Kristy Stark
Champlain College SDEV-435-81

planting_year manages data updates for annual changeover
Last Revised 8/3/24
'''


import data_connection  # manages connection to server
import plant


planting_plan_query = 'QueryPlantingPlan'
plant_requirements_query = 'RetrievePlantRequirements'
seasons_query = 'RetrieveMySeasonData'
plot_data_query = 'RetrievePlotData'
complete_set_query = 'CompleteYearPlantset'
increment_nitrogen_query = 'IncrementPlotNitrogen'


class PlantingYear:
    def __init__(self):
        self.plant_set_list = []
        self.plot_list = []
        self.master_plant_list = []

        self.my_year = None

    def display_plant_set_list(self):
        for plant in self.plant_set_list:
            plant.display_plant_set()

    def display_plot_list(self):
        for plot in self.plot_list:
            plot.display_plot()

    def display_master_plant_list(self):
        for plant in self.master_plant_list:
            plant.display_plant()

    def import_year_data(self, my_year):
        self.my_year = int(my_year)
        self.season_text = None
        self.season_year = None

    def generate_master_plant_list(self):

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(plant_requirements_query)
        records = cursor.fetchall()

        for r in records:
            print(r[0])

        for r in records:
            plant_id = r[0]
            plant_name = r[1]
            space_required_seedling = r[2]
            space_required_seeds = r[3]
            depth_requirement = r[4]
            sun_id = r[5]
            soil_moisture_id = r[6]
            crop_nitrogen_level = r[7]
            plant_in_spring = r[8]
            plant_in_fall = r[9]
            frost_tolerance_id = r[10]
            total_times_planted = r[11]
            times_succeeded = r[12]

            this_plant = plant.Plant()

            print(this_plant)

            this_plant.set_plant_requirements(plant_id,
                                                   plant_name,
                                                   space_required_seedling,
                                                   space_required_seeds,
                                                   depth_requirement,
                                                   sun_id,
                                                   soil_moisture_id,
                                                   crop_nitrogen_level,
                                                   plant_in_spring,
                                                   plant_in_fall,
                                                   frost_tolerance_id,
                                                   total_times_planted,
                                                   times_succeeded)

            this_plant.display_plant()  # for testing only

            self.master_plant_list.append(this_plant)

    def generate_plot_list(self):

        self.plot_list = []

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(plot_data_query)
        records = cursor.fetchall()
        for r in records:
            plot_id = r[0]
            self.plot_list.append(plot_id)

        return self.plot_list

    def complete_planting_year(self,
                               plant_set_list):

        self.generate_master_plant_list()

        for set in plant_set_list:
            print('about to display set')
            set.display_plant_set()

            # retrieve values previously pulled from SQL
            self.plant_id = set.plant_id
            outcome = set.outcome
            if outcome is True:
                self.success = 1
            else:
                self.success = 0
            self.plot_id = set.plot_id
            self.season_id = set.my_season_id

            self.nitrogen_change = None

            for plant in self.master_plant_list:
                if plant.plant_id == self.plant_id:
                    self.nitrogen_change = plant.crop_nitrogen_level
                    break

            print(self.plant_id)
            print(self.success)
            print(self.plot_id)
            print(self.nitrogen_change)
            print(self.season_id)

            this_connection = data_connection.Connection()  # connect to server
            cursor = this_connection.connection.cursor()  # set connection cursor

            # execute stored procedure to export to database using inputs

            (cursor.execute
             (complete_set_query + ' ?, ?, ?, ?, ?',
              [self.plant_id,
               self.success,
               self.plot_id,
               self.nitrogen_change,
               self.season_id]))

            cursor.commit()  # finalize entry into table

            print('Finished Updating Plant ID: ' + str(self.plant_id))  # confirmation

            this_connection.end_connection()

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        # execute stored procedure to export to database using inputs

        self.plot_list = self.generate_plot_list()
        for plot in self.plot_list:
            (cursor.execute
             (increment_nitrogen_query + ' ?',
              [plot]))

            cursor.commit()  # finalize entry into table

            print('Nitrogen incremented for plot ID: ' + str(plot))

        this_connection.end_connection()
