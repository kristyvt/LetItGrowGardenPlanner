import data_connection  # manages connection to server
import plant
import plant_set
import plot

planting_plan_query = 'QueryPlantingPlan'
plant_requirements_query = 'RetrievePlantRequirements'
seasons_query = 'RetrieveMySeasonData'
plot_data_query = 'RetrievePlotData'


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
            plot.display_plot()

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
        if plot_soil_moisture_id == crop_soil_moisture_requirement:
            print('Meets Soil moisture Requirement')
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

    def check_space_requirement(self,
                                space_required_seedling,
                                space_required_seeds,
                                plot_size,
                                measurement_unit_id,
                                crop_quantity,
                                crop_set_type,
                                is_container,
                                depth_requirement,
                                container_depth):

        if measurement_unit_id == 2:  # measurement ID 2 is feet
            plot_size = plot_size * 12  # convert to inches

        # 1 is seedlings
        if crop_set_type == 1:
            space_required = space_required_seedling * crop_quantity

        # 2 and 3 are seeds and bulbs respectively
        else:
            space_required = space_required_seeds * crop_quantity

        print('plot size is ' + str(plot_size))
        print('space_required is ' + str(space_required))

        # check for adequate distance between plants
        if space_required > plot_size:
            return False

        # if the plot being checked is a container, check its depth
        if is_container:
            print('plot is a container')
            if depth_requirement > container_depth:
                return False
            else:
                return True  # passes container depth check
        else:
            print('plot is not a container')
        return True  # passed all applicable spacing checks

    def check_requirements(self,
                           crop_nitrogen_level,
                           plot_nitrogen_level,
                           crop_sun_requirement,
                           plot_sun_id,
                           crop_soil_moisture_requirement,
                           plot_soil_moisture_id,
                           space_required_seedling,
                           space_required_seeds,
                           plot_size,
                           measurement_unit_id,
                           crop_quantity,
                           crop_set_type,
                           is_container,
                           depth_requirement,
                           container_depth):

        if not self.check_nitrogen_level(crop_nitrogen_level,
                                         plot_nitrogen_level):
            return False

        if not self.check_sun_requirement(crop_sun_requirement,
                                          plot_sun_id):
            return False

        if not self.check_soil_moisture_requirement(crop_soil_moisture_requirement,
                                                    plot_soil_moisture_id):
            return False

        if not self.check_space_requirement(space_required_seedling,
                                            space_required_seeds,
                                            plot_size,
                                            measurement_unit_id,
                                            crop_quantity,
                                            crop_set_type,
                                            is_container,
                                            depth_requirement,
                                            container_depth):
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
                plot.plot_status = 'taken'  # need to fix this so that it's only "taken" for that season
                return False  # or set a different variable for the plot status per season
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

        for plant in self.plant_set_list:

            this_plant_id = plant.plant_id
            crop_quantity = plant.set_quantity
            crop_set_type = plant.set_type_id
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
                                                                                   plot.soil_moisture_id,
                                                                                   space_required_seedling,
                                                                                   space_required_seeds,
                                                                                   plot.plot_size,
                                                                                   plot.measurement_unit_id,
                                                                                   crop_quantity,
                                                                                   crop_set_type,
                                                                                   plot.is_container,
                                                                                   depth_requirement,
                                                                                   plot.container_depth):
                            for p in self.plant_set_list:
                                print('plant in list is ' + str(p.plant_id))
                                print('plant to check is ' + str(this_plant_id))
                                if int(p.plant_id) == int(this_plant_id):
                                    print('matches')
                                    p.add_plot_id(plot.plot_id)
                                    p.add_season_id(season)
                                    p.export_plant_set(p.set_quantity,
                                                       p.plant_id,
                                                       p.my_season_id,
                                                       p.plot_id,
                                                       p.set_type_id)
                                    plot.plot_status = 'taken'
                                    self.plant_status = 'assigned'
                                    break
                            break

                        else:
                            continue

    def manual_plan(self,
                    new_plant_set,
                    season_id,
                    plot_id,
                    zone_id,
                    row,
                    column):

        print('start manual')

        self.this_plant_set = new_plant_set

        this_plant_id = self.this_plant_set.plant_id
        crop_quantity = self.this_plant_set.set_quantity
        crop_set_type = self.this_plant_set.set_type_id
        this_season_id = season_id

        if plot_id is not None:
            this_plot_id = int(plot_id)
        else:
            this_plot_id = 0
        if zone_id is not None:
            this_zone_id = int(zone_id)
        else:
            this_zone_id = 0
        if row is not None:
            this_row = int(row)
        else:
            this_row = 0
        if column is not None:
            this_column = int(column)
        else:
            this_column = 0

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

        self.generate_master_plant_list()

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

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(plot_data_query)
        records = cursor.fetchall()
        for r in records:
            plot_id = r[0]
            plot_size = r[1]
            measurement_unit_id = r[2]
            is_container = r[3]
            container_depth = r[4]
            plot_nitrogen_level = r[5]
            zone_id = r[6]
            sun_id = r[7]
            soil_moisture_id = r[8]
            plot_row = r[9]
            plot_column = r[10]
            plot_active = r[11]

            self.detailed_plot = plot.Plot()
            self.detailed_plot.set_plot_values(
                plot_id,
                plot_size,
                measurement_unit_id,
                is_container,
                container_depth,
                plot_nitrogen_level,
                zone_id,
                sun_id,
                soil_moisture_id,
                plot_row,
                plot_column,
                plot_active)

            self.plot_list.append(self.detailed_plot)

            print("plot ID is: " + str(plot_id))

        self.plot_to_check = self.get_plot(this_plot_id,
                                           this_row,
                                           this_column,
                                           this_zone_id)
        
        self.plot_to_check.display_plot()

        self.plot_to_check.plot_status = None

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        if (self.is_empty(self.plot_to_check, this_season_id)
                and self.check_requirements(crop_nitrogen_level,
                                            self.plot_to_check.plot_nitrogen_level,
                                            sun_id,
                                            self.plot_to_check.sun_id,
                                            soil_moisture_id,
                                            self.plot_to_check.soil_moisture_id,
                                            space_required_seedling,
                                            space_required_seeds,
                                            self.plot_to_check.plot_size,
                                            self.plot_to_check.measurement_unit_id,
                                            crop_quantity,
                                            crop_set_type,
                                            self.plot_to_check.is_container,
                                            depth_requirement,
                                            self.plot_to_check.container_depth)):

            self.this_plant_set.add_plot_id(this_plot_id)
            self.this_plant_set.add_season_id(this_season_id)
            self.this_plant_set.export_plant_set(crop_quantity,
                                                this_plant_id,
                                                this_season_id,
                                                this_plot_id,
                                                crop_set_type)
            self.plot_to_check.plot_status = 'taken'

            print('export complete')

        else:
            print('failed checks. not exported')

    def get_plot(self,
                 this_plot_id,
                 plot_row,
                 plot_column,
                 zone_id):
        for plot in self.plot_list:
            print(this_plot_id)
            print(plot_row)
            print(plot_column)
            print(zone_id)
            print(plot.plot_id)
            print(plot.plot_row)
            print(plot.plot_column)
            print(plot.zone_id)

            if this_plot_id > 0:
                if this_plot_id == plot.plot_id:
                    return plot
            else:
                if plot_row == plot.plot_row and plot_column == plot.plot_column and zone_id == plot.zone_id:
                    print('found it')
                    return plot
                else:
                    continue
