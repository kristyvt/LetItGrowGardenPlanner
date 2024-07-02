import data_connection  # manages connection to server

add_plot_query = 'AddPlot'


class Plot:
    def __init__(self):
        self.plot_id = None
        self.plot_size = None
        self.measurement_unit_id = None
        self.is_container = None
        self.container_depth = None
        self.plot_nitrogen_level = None
        self.zone_id = None
        self.sun_id = None
        self.soil_moisture_id = None
        self.plot_row = None
        self.plot_column = None
        self.plot_active = None
        self.plot_status = None

    def set_plot_values(
            self,
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
            plot_active):
        self.plot_id = int(plot_id)
        self.plot_size = int(plot_size)
        self.measurement_unit_id = int(measurement_unit_id)
        self.is_container = bool(is_container)
        if self.is_container:
            self.container_depth = float(container_depth)
        self.plot_nitrogen_level = int(plot_nitrogen_level)
        self.zone_id = int(zone_id)
        self.sun_id = int(sun_id)
        self.soil_moisture_id = int(soil_moisture_id)
        self.plot_row = plot_row
        self.plot_column = plot_column
        self.plot_active = bool(plot_active)

    def display_plot(self):
        print(self.__dict__)  # mostly for testing, DELETE before submission

    def export_plot(self,
                    plot_id,
                    plot_size,
                    measurement_unit_id,
                    is_container,
                    container_depth,
                    zone_id,
                    sun_id,
                    soil_moisture_id,
                    plot_row,
                    plot_column
                    ):
        self.plot_id = int(plot_id)
        self.plot_size = int(plot_size)
        self.measurement_unit_id = int(measurement_unit_id)
        self.is_container = bool(is_container)
        self.container_depth = container_depth
        self.zone_id = int(zone_id)
        self.sun_id = int(sun_id)
        self.soil_moisture_id = int(soil_moisture_id)
        self.plot_row = int(plot_row)
        self.plot_column = int(plot_column)

        # execute stored procedure to add new plot to database using inputs

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        (cursor.execute
         (add_plot_query + ' ?, ?, ?, ?, ?, ?, ?, ?, ?, ?',
          [self.plot_id,
           self.plot_size,
           self.measurement_unit_id,
           self.is_container,
           self.container_depth,
           self.zone_id,
           self.sun_id,
           self.soil_moisture_id,
           self.plot_row,
           self.plot_column,
           ]))

        cursor.commit()  # finalize entry into table

        print('Finished Inserting Plot ID number ' + str(self.plot_id))  # confirmation

        this_connection.end_connection()

    def get_plot(self, this_plot_id, plot_row, plot_column, this_zone_id):


        pass
