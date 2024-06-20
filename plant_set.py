from datetime import datetime

import data_connection  # manages connection to server


class PlantSet:
    def __init__(self):
        self.set_quantity = None
        self.plant_id = None
        self.my_season_id = None
        self.plot_id = None
        self.set_type_id = None

    def add_new_plant_set(self, plant_id, set_type_id, set_quantity):
        self.plant_id = int(plant_id)
        self.set_quantity = int(set_quantity)
        self.set_type_id = int(set_type_id)

    def display_plant_set(self):
        print(self.__dict__)  # mostly for testing, DELETE before submission

    def add_plot_id(self, plot_id):
        self.plot_id = int(plot_id)

    def add_season_id(self, season_id):
        self.my_season_id = int(season_id)


