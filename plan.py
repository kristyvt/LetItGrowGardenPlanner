import data_connection  # manages connection to server
import plant
import plant_set
import plot

planting_plan_query = 'QueryPlantingPlan'
plant_requirements_query = 'RetrievePlantRequirements'
seasons_query = 'RetrieveMySeasonData'


class Plan:
    def __init__(self):
        self.plant_set_list = []
        self.plot_list = []
        self.master_plant_list = []

    def display_plant_set_list(self):
        for plant in self.plant_set_list:
            plant.display_plant_set()

    def display_plot_list(self):
        for plot in self.plot_list:
            plot.display_plot_set()

    def display_master_plant_list(self):
        for plant in self.master_plant_list:
            plant.display_plant()

    def generate_master_plant_list(self):

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(plant_requirements_query)
        records = cursor.fetchall()
        for r in records:
            plant_id = r[0]
            plant_name = r[1]
            space_required_seedling = r[2]
            space_required_seeds = r[3]
            depth_requirement = r[4]
            sun_id = r[5]
            soil_moisture_id = r[6]
            crop_nitrogen_level = r[7]
            always_include = r[8]
            plant_in_spring = r[9]
            plant_in_fall = r[10]
            frost_tolerance_id = r[11]
            total_times_planted = r[12]
            times_succeeded = r[13]

            self.this_plant = plant.Plant()
            self.this_plant.set_plant_requirements(plant_id,
                                                   plant_name,
                                                   space_required_seedling,
                                                   space_required_seeds,
                                                   depth_requirement,
                                                   sun_id,
                                                   soil_moisture_id,
                                                   crop_nitrogen_level,
                                                   always_include,
                                                   plant_in_spring,
                                                   plant_in_fall,
                                                   frost_tolerance_id,
                                                   total_times_planted,
                                                   times_succeeded)

            self.master_plant_list.append(self.this_plant)

    def check_nitrogen_level(self,
                             crop_nitrogen_level,
                             plot_nitrogen_level):

        if (plot_nitrogen_level + crop_nitrogen_level) >= -1:
            print('nitrogen level sufficient, excess nitrogen is:'
                  + str((plot_nitrogen_level + crop_nitrogen_level + 1)))
            return True
        else:
            print('insufficient nitrogen, difference is '
                  + (str(plot_nitrogen_level + crop_nitrogen_level + 1)))
            return False

    def check_soil_moisture_requirement(self,
                                        crop_soil_moisture_requirement,
                                        plot_soil_moisture_id):
        if ((plot_soil_moisture_id - crop_soil_moisture_requirement >= -1)
                and (plot_soil_moisture_id - crop_soil_moisture_requirement <= 1)):
            print('Soil moisture level within acceptable range (1 level):'
                  + str((plot_soil_moisture_id - crop_soil_moisture_requirement)))
            return True
        else:
            print('Excessive difference in soil moisture level of '
                  + (str(plot_soil_moisture_id - crop_soil_moisture_requirement)))
            return False

    def check_sun_requirement(self,
                              crop_sun_requirement,
                              plot_sun_id):
        if plot_sun_id == crop_sun_requirement:
            print('Meets Sun Requirement')
            return True
        else:
            print('Excessive difference in sun level of '
                  + (str(plot_sun_id - crop_sun_requirement)))
            return False

    def check_requirements(self,
                           crop_nitrogen_level,
                           plot_nitrogen_level,
                           crop_sun_requirement,
                           plot_sun_id,
                           crop_soil_moisture_requirement,
                           plot_soil_moisture_id):

        if not self.check_nitrogen_level(crop_nitrogen_level,
                                         plot_nitrogen_level):
            return False

        if not self.check_sun_requirement(crop_sun_requirement,
                                          plot_sun_id):
            return False

        if not self.check_soil_moisture_requirement(crop_soil_moisture_requirement,
                                                    plot_soil_moisture_id):
            return False

        return True

    def is_empty(self, plot, season):

        self.status = None

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(planting_plan_query)
        records = cursor.fetchall()
        for r in records:
            season_id = r[0]
            season_text = r[1]
            plant = r[2]
            zone = r[3]
            plot_number = r[4]
            space_seeds = r[5]
            space_seedlings = r[6]
            depth_required = r[7]

            print(r)
            print('Season ID assigned to plot is' + str(season_id))
            print('Season ID iteration to check is' + str(season))

            if plot.plot_id == plot_number \
                    and season_id == season:
                print('plot ' + str(plot.plot_id) + ' is taken')
                self.status = 'taken'
                plot.plot_status = 'taken'                          # need to fix this so that it's only "taken" for that season
                return False                                        # or set a different variable for the plot status per season
            else:
                print('plot ' + str(plot.plot_id) + ' is empty')
                self.status = 'empty'
                print('plot to check ' + str(plot.plot_id))
                print('plot in list ' + str(plot_number))

        if self.status == 'empty' and plot.plot_status != 'taken':
            print('plot ' + str(plot.plot_id) + ' is fully empty')
            self.plot_status = 'empty'
            return True

    def execute_plan(self):

        self.generate_master_plant_list()
        self.display_master_plant_list()

        for plant in self.plant_set_list:

            this_plant_id = plant.plant_id
            space_required_seedling = None
            space_required_seeds = None
            depth_requirement = None
            sun_id = None
            soil_moisture_id = None
            crop_nitrogen_level = None
            always_include = None
            plant_in_spring = None
            plant_in_fall = None
            frost_tolerance_id = None
            total_times_planted = None
            times_succeeded = None

            for p in self.master_plant_list:
                if p.plant_id == this_plant_id:
                    space_required_seedling = p.space_required_seedling
                    space_required_seeds = p.space_required_seeds
                    depth_requirement = p.depth_requirement
                    sun_id = p.sun_id
                    soil_moisture_id = p.soil_moisture_id
                    crop_nitrogen_level = p.crop_nitrogen_level
                    always_include = p.always_include
                    plant_in_spring = p.plant_in_spring
                    plant_in_fall = p.plant_in_fall
                    frost_tolerance_id = p.frost_tolerance_id
                    total_times_planted = p.total_times_planted
                    times_succeeded = p.times_succeeded

            print(space_required_seedling)
            print(space_required_seeds)
            print(depth_requirement)
            print(sun_id)
            print(soil_moisture_id)
            print(crop_nitrogen_level)
            print(always_include)
            print(plant_in_spring)
            print(plant_in_fall)
            print(frost_tolerance_id)
            print(total_times_planted)
            print(times_succeeded)

            self.plot_status = None
            self.plant_status = None

            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            season_list = []
            cursor.execute(seasons_query)
            records = cursor.fetchall()
            for r in records:
                this_season_id = r[0]
                season_list.append(this_season_id)
            print(season_list)

            for season in season_list:

                for plot in self.plot_list:
                    plot.plot_status = None

                if self.plant_status == 'assigned':
                    break
                else:

                    for plot in self.plot_list:

                        if self.is_empty(plot, season) and self.check_requirements(crop_nitrogen_level,
                                                                                   plot.plot_nitrogen_level,
                                                                                   sun_id,
                                                                                   plot.sun_id,
                                                                                   soil_moisture_id,
                                                                                   plot.soil_moisture_id):
                            for p in self.plant_set_list:
                                print('plant in list is ' + str(p.plant_id))
                                print('plant to check is ' + str(this_plant_id))
                                if int(p.plant_id) == int(this_plant_id):
                                    print('matches')
                                    p.add_plot_id(plot.plot_id)
                                    p.add_season_id(season)
                                    plot.plot_status = 'taken'
                                    self.plant_status = 'assigned'
                                    break
                            break

                        else:
                            continue
