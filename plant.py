'''
Class to manage the master list of plants
that the user can choose from.

Includes functions to add new plants to the master list
and edit details related to exiting plants.
'''

import data_connection  # manages connection to server

# plant class object variables correspond to fields in SQL plant table
class Plant:
    def __init__(self):
        self.plant_name = None
        self.crop_group_id = None
        self.crop_nitrogen_level = None
        self.sun_id = None
        self.soil_moisture_id = None
        self.frost_tolerance_id = None
        self.space_required_seeds = None
        self.space_required_seedling = None
        self.depth_requirement = None
        self.depth_to_plant_seeds = None
        self.watering_requirement_id = None
        self.plant_in_spring = None
        self.plant_in_fall = None
        self.days_to_harvest = None
        self.plant_active = None
        self.times_succeeded = None
        self.total_times_planted = None

    # function to add a new plant to the master table of plants

    def add_plant(self,
                  plant_name,
                  crop_group_id,
                  sun_id,
                  soil_moisture_id,
                  frost_tolerance_id,
                  space_required_seedling,
                  space_required_seeds,
                  depth_requirement,
                  depth_to_plant_seeds,
                  watering_requirement_id,
                  plant_in_spring,
                  plant_in_fall,
                  days_to_harvest):
        self.plant_name = plant_name
        self.crop_group_id = crop_group_id
        self.sun_id = sun_id
        self.soil_moisture_id = soil_moisture_id
        self.frost_tolerance_id = frost_tolerance_id
        self.space_required_seedling = space_required_seedling
        self.space_required_seeds = space_required_seeds
        self.depth_requirement = depth_requirement
        self.depth_to_plant_seeds = depth_to_plant_seeds
        self.watering_requirement_id = watering_requirement_id
        self.plant_in_spring = plant_in_spring
        self.plant_in_fall = plant_in_fall
        self.days_to_harvest = days_to_harvest

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        # execute stored procedure to add new plant to database using inputs

        (cursor.execute
         ('AddPlant ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?',
          [self.plant_name,
           self.plant_in_spring,
           self.plant_in_fall,
           self.days_to_harvest,
           self.space_required_seedling,
           self.space_required_seeds,
           self.depth_requirement,
           self.depth_to_plant_seeds,
           self.crop_group_id,
           self.sun_id,
           self.soil_moisture_id,
           self.frost_tolerance_id,
           self.watering_requirement_id]))

        cursor.commit()  # finalize entry into table

        success_message = 'Finished Inserting ' + self.plant_name

        self.display_plant()

        this_connection.end_connection()

        return success_message

    def display_plant(self):
        print(self.__dict__)  # mostly for testing, DELETE before submission


    def set_plant_requirements(self,
                  plant_id,
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
                  times_succeeded):

        print('setting requirements')

        self.plant_id = plant_id
        self.plant_name = plant_name
        self.space_required_seedling = space_required_seedling
        self.space_required_seeds = space_required_seeds
        self.depth_requirement = depth_requirement
        self.sun_id = sun_id
        self.soil_moisture_id = soil_moisture_id
        self.crop_nitrogen_level = crop_nitrogen_level
        self.plant_in_spring = plant_in_spring
        self.plant_in_fall = plant_in_fall
        self.frost_tolerance_id = frost_tolerance_id
        self.total_times_planted = total_times_planted
        self.times_succeeded = times_succeeded