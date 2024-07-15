import data_connection  # manages connection to server

add_plot_query = 'AddPlot'
retrieve_plot_query = 'QuerySinglePlotData'
update_plot_query = 'UpdatePlot'

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

    def import_plot(self, this_plot_id):
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

        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(retrieve_plot_query + ' ?',
                       [this_plot_id])

        records = cursor.fetchall()
        for r in records:
            self.plot_id = r[0]
            self.plot_size = r[1]
            self.measurement_unit_id = r[2]
            self.is_container = r[3]
            self.container_depth = r[4]
            self.plot_nitrogen_level = r[5]
            self.zone_id = r[6]
            self.sun_id = r[7]
            self.soil_moisture_id = r[8]
            self.plot_row = r[9]
            self.plot_column = r[10]
            self.plot_active = r[11]

            if self.plot_id is None:
                print('not found')

            else:
                self.plot_id = r[0]
                print(r)
                print(r[0])
                break

        return self.plot_id

    # function to export updated plot details to SQl database
    def export_updated_plot(self,
                            plot_id,
                            plot_size,
                            measurement_unit_id,
                            is_container,
                            container_depth,
                            plot_nitrogen_level,
                            sun_id,
                            soil_moisture_id,
                            plot_active):
        self.plot_id = int(plot_id)
        self.plot_size = int(plot_size)
        self.measurement_unit_id = int(measurement_unit_id)
        self.is_container = bool(is_container)
        self.container_depth = container_depth
        self.plot_nitrogen_level = int(plot_nitrogen_level)
        self.sun_id = int(sun_id)
        self.soil_moisture_id = int(soil_moisture_id)
        self.plot_active = bool(plot_active)

        print('Start export')

        # execute stored procedure to update plot to database using inputs

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        (cursor.execute
         (update_plot_query + ' ?, ?, ?, ?, ?, ?, ?, ?, ?',
          [self.plot_id,
           self.plot_size,
           self.measurement_unit_id,
           self.is_container,
           self.container_depth,
           self.plot_nitrogen_level,
           self.sun_id,
           self.soil_moisture_id,
           self.plot_active
           ]))

        cursor.commit()  # finalize entry into table

        print('Finished Updating Plot ID number ' + str(self.plot_id))  # confirmation

        this_connection.end_connection()



