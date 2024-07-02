import tkinter as tk  #see notes below on what needs fixing to add plant FINISH FUNCTION TO ADD MANUAL PLAN
import os
from tkinter import ttk
import data_connection  # manages connection to server
import plan
import plant
import plant_set
import plot

LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)

# SQL queries used to populate dropdown lists

plant_name_query = 'RetrievePlantNames'
set_type_query = 'RetrieveSetTypes'
plot_data_query = 'RetrievePlotData'
crop_group_query = 'RetrieveCropGroupData'
frost_tolerance_query = 'RetrieveFrostToleranceData'
sun_query = 'RetrieveSunData'
soil_moisture_query = 'RetrieveSoilMoistureData'
watering_requirement_query = 'RetrieveWateringRequirementData'
zone_query = 'RetrieveZoneData'
add_zone_query = 'AddZone'
measurement_unit_query = 'RetrieveMeasurementUnitData'
plant_detail_query = 'QueryAllPlantsSetupDetail'
planting_plan_query = 'QueryPlantingPlan'
seasons_query = 'RetrieveMySeasonData'
display_grid_query = 'QueryPlotGrid'

logo_file = "WelcomeLogo.png"
icon_file = "Icon.png"


# class to manage all dropdown lists

class DropDown:
    def __init__(self, parent, query_name, row, column, columnspan, sticky):
        self.this_connection = data_connection.Connection()
        self.cursor = self.this_connection.connection.cursor()

        self.drop_down_list = []
        self.selection = None
        self.id = None

        self.cursor.execute(query_name)
        records = self.cursor.fetchall()
        for r in records:
            drop_down_value = r[1]
            self.drop_down_list.append(drop_down_value)

        self.combo = ttk.Combobox(parent,
                                  values=self.drop_down_list)
        self.combo.grid(row=row,
                        column=column,
                        columnspan=columnspan,
                        sticky=sticky)
        self.combo.set('Select Value')
        self.combo.bind('<<ComboboxSelected>>', self.get_value)

    def get_value(self, event):
        print(self.combo.get())
        self.selection = self.combo.get()
        print(self.selection)

    def get_id(self, query_name, value):
        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor
        cursor.execute(query_name)
        records = cursor.fetchall()
        for r in records:
            if value == r[1]:
                self.id = r[0]
                this_connection.end_connection()
                return self.id


class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title("Let it Grow Garden Planner")
        img = tk.PhotoImage(file=icon_file)
        self.iconphoto(False, img)

        container.pack(side="top",
                       fill="both",
                       expand=True)

        container.grid_rowconfigure(0,
                                    weight=1)
        container.grid_columnconfigure(0,
                                       weight=1)

        self.frames = {}

        for F in (StartPage,
                  AddPlantPage,
                  EditSetPage,
                  DisplayPlants,
                  DisplayPlan,
                  GardenPlanPage,
                  SetupPage,
                  ConfigureZonesPage,
                  AddPlotsPage):
            frame = F(container,
                      self)

            self.frames[F] = frame

            frame.grid(row=0,
                       column=0,
                       sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def close_window(self):
        exit()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        path = os.path.abspath(__file__)
        logo_dir = os.path.dirname(path)
        logo_path = os.path.join(logo_dir, logo_file)

        logo = tk.PhotoImage(file=logo_path)
        label = tk.Label(image=logo)
        label.image = logo

        label = tk.Label(self,
                         image=label.image)
        label.grid(row=1,
                   column=1,
                   columnspan=4)

        button = tk.Button(self,
                           width=30,
                           text="Garden Setup",
                           command=lambda: controller.show_frame(SetupPage))
        button.grid(row=2,
                    column=1,
                    sticky='E')

        button = tk.Button(self,
                           width=30,
                           text="Add Plant",
                           command=lambda: controller.show_frame(AddPlantPage))
        button.grid(row=2,
                    column=2,
                    sticky='W')

        button = tk.Button(self,
                           width=30,
                           text="Plant Information",
                           command=lambda: controller.show_frame(DisplayPlants))
        button.grid(row=3, column=2, sticky='E')

        button = tk.Button(self,
                           width=30,
                           text="Start Garden Plan",
                           command=lambda: controller.show_frame(GardenPlanPage))
        button.grid(row=2,
                    column=3,
                    sticky='E')

        button = tk.Button(self,
                           width=30,
                           text="Edit Plant Set",
                           command=lambda: controller.show_frame(EditSetPage))
        button.grid(row=3,
                    column=3,
                    sticky='E')

        button = tk.Button(self,
                           width=30,
                           text="View Garden Plan",
                           command=lambda: controller.show_frame(DisplayPlan))
        button.grid(row=2,
                    column=4,
                    sticky='E')

        button = tk.Button(self,
                           width=30,
                           text="Exit",
                           command=lambda: controller.close_window())
        button.grid(row=3,
                    column=4,
                    sticky='E')

        for child in self.winfo_children():
            child.grid_configure(padx=10,
                                 pady=10)


class AddPlantPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = (tk.Label
                 (self,
                  text="Add Plant",
                  font=LARGE_FONT))
        label.grid(row=1,
                   column=2,
                   columnspan=4)

        label = tk.Label(self, text=" ")
        label.grid(row=2,
                   column=1)

        label = tk.Label(self,
                         text="Plant Name:",
                         justify=tk.RIGHT,
                         anchor='e'
                         )
        label.grid(row=3,
                   column=1,
                   columnspan=2)
        self.plant_name_entry = tk.Entry(self,
                                         justify=tk.LEFT,
                                         width=40,
                                         )
        self.plant_name_entry.grid(row=3,
                                   column=3,
                                   columnspan=2)

        self.always_include = tk.IntVar()
        self.always_include_checkbox = (tk.Checkbutton(self,
                                                       text="Include every year?",
                                                       variable=self.always_include,
                                                       onvalue=1,
                                                       offvalue=0,
                                                       width=20,
                                                       justify=tk.LEFT,
                                                       anchor='w'))
        self.always_include_checkbox.grid(row=3,
                                          column=5)

        self.plant_spring = tk.IntVar()
        self.spring_checkbox = (tk.Checkbutton(self,
                                               text="Plant in Spring",
                                               variable=self.plant_spring,
                                               onvalue=1,
                                               offvalue=0,
                                               width=20,
                                               justify=tk.LEFT,
                                               anchor='w'))
        self.spring_checkbox.grid(row=3,
                                  column=6)

        self.plant_fall = tk.IntVar()
        self.fall_checkbox = (tk.Checkbutton(self,
                                             text="Plant in Fall",
                                             variable=self.plant_fall,
                                             onvalue=1,
                                             offvalue=0,
                                             width=20,
                                             justify=tk.LEFT,
                                             anchor='w'))
        self.fall_checkbox.grid(row=3,
                                column=7)

        label = tk.Label(self,
                         text=" ")
        label.grid(row=4,
                   column=1)

        label = tk.Label(self,
                         text="Crop Rotation Group:")
        label.grid(row=5,
                   column=1,
                   columnspan=2)
        self.crop_group_combo = DropDown(self,
                                         crop_group_query,
                                         5,
                                         3,
                                         1,
                                         'W')

        label = tk.Label(self,
                         text="Frost Tolerance:")
        label.grid(row=5,
                   column=4,
                   columnspan=2)
        self.frost_tolerance_combo = DropDown(self,
                                              frost_tolerance_query,
                                              5,
                                              6,
                                              1,
                                              'W')

        label = tk.Label(self,
                         text="", )
        label.grid(row=6,
                   column=1)

        label = tk.Label(self,
                         text="Sun Required:")
        label.grid(row=7,
                   column=1,
                   columnspan=2)
        self.sun_combo = DropDown(self,
                                  sun_query,
                                  7,
                                  3,
                                  1,
                                  'W')

        label = tk.Label(self,
                         text="Soil Moisture Required:")
        label.grid(row=7,
                   column=4,
                   columnspan=2)
        self.soil_moisture_combo = DropDown(self,
                                            soil_moisture_query,
                                            7,
                                            6,
                                            1,
                                            'W')

        label = tk.Label(self,
                         text=" ")
        label.grid(row=8,
                   column=1)

        label = tk.Label(self,
                         text=" ")
        label.grid(row=9,
                   column=1)

        label = tk.Label(self,
                         text="Space per Seedling, in inches:",
                         anchor='e',
                         justify=tk.RIGHT)
        label.grid(row=9,
                   column=2,
                   columnspan=2)

        self.space_per_seedling_entry = tk.Entry(self,
                                                 width=5,
                                                 justify=tk.LEFT)
        self.space_per_seedling_entry.grid(row=9,
                                           column=4)

        label = tk.Label(self,
                         text=" ")
        label.grid(row=10,
                   column=1)

        label = tk.Label(self,
                         text="Space per Seed Pack, in inches:",
                         anchor='e',
                         justify=tk.RIGHT)
        label.grid(row=10,
                   column=2,
                   columnspan=2)

        self.space_per_seedpack_entry = tk.Entry(self,
                                                 width=5,
                                                 justify=tk.LEFT)
        self.space_per_seedpack_entry.grid(row=10,
                                           column=4)

        label = tk.Label(self,
                         text="Depth Required per Plant, in inches:",
                         anchor='e',
                         justify=tk.RIGHT)
        label.grid(row=9,
                   column=5,
                   columnspan=2)

        self.depth_per_plant_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT)
        self.depth_per_plant_entry.grid(row=9,
                                        column=7)

        label = tk.Label(self,
                         text="Depth to Plant Seeds, inches, 2 decimals ok:",
                         anchor='e',
                         justify=tk.RIGHT)
        label.grid(row=10,
                   column=5,
                   columnspan=2)

        self.depth_for_seeds_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT)
        self.depth_for_seeds_entry.grid(row=10,
                                        column=7)

        label = tk.Label(self,
                         text=" ")
        label.grid(row=11,
                   column=1)

        label = tk.Label(self,
                         text=" ")
        label.grid(row=12,
                   column=1,
                   columnspan=2)

        label = tk.Label(self,
                         text="Days to Harvest:",
                         anchor='e',
                         justify=tk.RIGHT)
        label.grid(row=12,
                   column=3)

        self.days_to_harvest_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT)
        self.days_to_harvest_entry.grid(row=12,
                                        column=4)

        label = tk.Label(self,
                         text="Watering Frequency:")
        label.grid(row=12,
                   column=5,
                   columnspan=1)
        self.watering_requirement_combo = DropDown(self,
                                                   watering_requirement_query,
                                                   12,
                                                   6,
                                                   1,
                                                   'W')

        self.new_plant = plant.Plant()

        button = tk.Button(self, text="Add Plant",
                           command=self.add_new_plant)
        button.grid(row=12,
                    column=7)

        label = tk.Label(self,
                         text="")
        label.grid(row=13,
                   column=3)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=14,
                    column=7)

    def add_new_plant(self):
        self.plant_name = None
        self.crop_group_id = None
        self.sun_id = None
        self.soil_moisture_id = None
        self.frost_tolerance_id = None
        self.space_required_seeds = None
        self.space_required_seedling = None
        self.depth_requirement = None
        self.depth_to_plant_seeds = None
        self.watering_requirement_id = None
        self.always_include = None
        self.plant_in_spring = None
        self.plant_in_fall = None
        self.days_to_harvest = None
        self.indoors_date_range_id = None
        self.seeds_date_range_id = None
        self.seedlings_date_range_id = None
        self.fall_date_range_id = None
        self.plant_active = None
        self.times_succeeded = None
        self.total_times_planted = None

        self.plant_name = self.plant_name_entry.get()
        crop_group_text = self.crop_group_combo.selection
        self.crop_group_id = \
            int(self.crop_group_combo.get_id(crop_group_query,
                                             crop_group_text))
        sun_id_text = self.sun_combo.selection
        self.sun_id = int(self.sun_combo.get_id(sun_query,
                                                sun_id_text))
        soil_moisture_text = self.soil_moisture_combo.selection
        self.soil_moisture_id = \
            int(self.soil_moisture_combo.get_id(soil_moisture_query,
                                                soil_moisture_text))
        frost_tolerance_text = self.frost_tolerance_combo.selection
        self.frost_tolerance_id = \
            int(self.frost_tolerance_combo.get_id(frost_tolerance_query,
                                                  frost_tolerance_text))
        self.space_required_seeds = int(self.space_per_seedpack_entry.get())
        self.space_required_seedling = int(self.space_per_seedling_entry.get())
        self.depth_requirement = int(self.depth_per_plant_entry.get())
        self.depth_to_plant_seeds = float(self.depth_for_seeds_entry.get())
        watering_requirement_text = self.watering_requirement_combo.selection
        self.watering_requirement_id = \
            int(self.watering_requirement_combo.get_id(watering_requirement_query,
                                                       watering_requirement_text))

        self.plant_in_spring = bool(self.plant_spring.get())
        self.plant_in_fall = bool(self.plant_fall.get())
        self.days_to_harvest = int(self.days_to_harvest_entry.get())

        new_plant = plant.Plant()
        new_plant.add_plant(self.plant_name,
                            self.crop_group_id,
                            self.sun_id,
                            self.soil_moisture_id,
                            self.frost_tolerance_id,
                            self.space_required_seedling,
                            self.space_required_seeds,
                            self.depth_requirement,
                            self.depth_to_plant_seeds,
                            self.watering_requirement_id,
                            self.plant_in_spring,
                            self.plant_in_fall,
                            self.days_to_harvest)


class DisplayPlants(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,
                         text="All Available Plants",
                         font=LARGE_FONT)
        label.grid(row=1,
                   column=1,
                   columnspan=8)

        label = tk.Label(self,
                         text="Added new plants? Click to update the list: ",
                         anchor='e',
                         justify=tk.RIGHT)
        label.grid(row=1,
                   column=9,
                   columnspan=3)

        button = tk.Button(self,
                           text="Regenerate List",  # UNSURE IF THIS IS WORKING, NEED TO TEST FULLY
                           anchor='w',
                           justify=tk.LEFT,
                           command=lambda: self.query_all_plants(controller))
        button.grid(row=1,
                    column=12)

        label = tk.Label(self,
                         text=" ",
                         font=LARGE_FONT)
        label.grid(row=2,
                   column=2)

        label = tk.Label(self,
                         text="Plant Name")
        label.grid(row=3,
                   column=2)

        label = tk.Label(self,
                         text="In Plan?")
        label.grid(row=3,
                   column=3)

        label = tk.Label(self,
                         text="Crop Group")
        label.grid(row=3,
                   column=4)

        label = tk.Label(self,
                         text="Sun")
        label.grid(row=3,
                   column=5)

        label = tk.Label(self,
                         text="Soil Moisture")
        label.grid(row=3,
                   column=6)

        label = tk.Label(self,
                         text="Space per Seed Pack")
        label.grid(row=3,
                   column=7)

        label = tk.Label(self,
                         text="Space Per Seedling")
        label.grid(row=3,
                   column=8)

        label = tk.Label(self,
                         text="Depth Requirement")
        label.grid(row=3,
                   column=9)

        label = tk.Label(self,
                         text="Watering Frequency")
        label.grid(row=3,
                   column=10)

        label = tk.Label(self,
                         text="Frost Tolerance")
        label.grid(row=3,
                   column=11)

        label = tk.Label(self,
                         text="Time to Harvest")
        label.grid(row=3,
                   column=12)

        label = tk.Label(self,
                         text="Plant in Spring?")
        label.grid(row=3,
                   column=13)

        label = tk.Label(self,
                         text="Plant in Fall?")
        label.grid(row=3,
                   column=14)

        self.query_all_plants(controller)

    def query_all_plants(self, controller):
        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(plant_detail_query)

        for row_number, row in enumerate(cursor, 4):
            tk.Label(self, text=str(row[1])).grid(column=2, row=row_number)
            tk.Label(self, text=str(row[2])).grid(column=3, row=row_number)
            tk.Label(self, text=str(row[3])).grid(column=4, row=row_number)
            tk.Label(self, text=str(row[4])).grid(column=5, row=row_number)
            tk.Label(self, text=str(row[5])).grid(column=6, row=row_number)
            tk.Label(self, text=str(row[6]) + ' inches').grid(column=7, row=row_number)
            tk.Label(self, text=str(row[7]) + ' inches').grid(column=8, row=row_number)
            tk.Label(self, text=str(row[8]) + ' inches').grid(column=9, row=row_number)
            tk.Label(self, text=str(row[9])).grid(column=10, row=row_number)
            tk.Label(self, text=str(row[10])).grid(column=11, row=row_number)
            tk.Label(self, text=str(row[11]) + ' days').grid(column=12, row=row_number)
            tk.Label(self, text=str(row[12])).grid(column=13, row=row_number)
            tk.Label(self, text=str(row[13])).grid(column=14, row=row_number)

        this_connection.end_connection()

        label = tk.Label(self,
                         text=" ",
                         font=LARGE_FONT)
        label.grid(row=row_number + 1,
                   column=2)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=row_number + 2,
                    column=8)

    def reset_plant_dropdown(self):
        self.plant_combo = DropDown(self,
                                    plant_name_query,
                                    3,
                                    2,
                                    2,
                                    'W')


class GardenPlanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,
                         text="Create Garden Plan",
                         font=LARGE_FONT)
        label.grid(row=1,
                   column=2)

        label = tk.Label(self,
                         text="Please complete the following for all Garden Plans")
        label.grid(row=2,
                   column=1,
                   columnspan=5)

        label = tk.Label(self,
                         text="Select Plant Name:")
        label.grid(row=3,
                   column=1)

        self.plant_combo = DropDown(self,
                                    plant_name_query,
                                    3,
                                    2,
                                    3,
                                    'W')

        label = tk.Label(self,
                         text="Refresh the list if new plants have been added:")
        label.grid(row=3,
                   column=3,
                   columnspan=3)

        button = tk.Button(self,
                           text="Refresh Plants",
                           command=self.reset_plant_dropdown)
        button.grid(row=3,
                    column=7,
                    sticky='E')

        label = tk.Label(self,
                         text="Set Type:")
        label.grid(row=4,
                   column=1)

        self.set_type_combo = DropDown(self,
                                       set_type_query,
                                       4,
                                       2,
                                       1,
                                       'W')

        label = tk.Label(self,
                         text="Quantity:")
        label.grid(row=4,
                   column=3)
        self.quantity_entry = tk.Entry(self,
                                       width=5)
        self.quantity_entry.grid(row=4,
                                 column=4)

        button = tk.Button(self,
                           text="Add to Auto-Plan",
                           command=self.add)
        button.grid(row=4,
                    column=5,
                    sticky='E')

        button = tk.Button(self,
                           text="Complete Auto-Plan",
                           command=self.complete)
        button.grid(row=5,
                    column=5,
                    sticky='E')

        label = tk.Label(self,
                         text="For Manual Plans Only")
        label.grid(row=6,
                   column=1,
                   columnspan=2)

        label = tk.Label(self,
                         text="Select your Season:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=7,
                   column=1,
                   columnspan=2)

        self.season_combo = DropDown(self,
                                     seasons_query,
                                     7,
                                     3,
                                     2,
                                     'W')

        self.plot_stat_list = []
        top_plot_id = 1
        top_zone_id = 1
        top_row = 1
        top_column = 1

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

            self.this_plot = plot.Plot()
            self.this_plot.set_plot_values(
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

            self.plot_stat_list.append(self.this_plot)

            if r[11] == 0:
                continue
            else:
                if r[0] > top_plot_id:  # add a popup with message to create plots first if no plots are set up yet
                    top_plot_id = r[0]

                if r[6] is None:
                    continue
                else:
                    if r[6] > top_zone_id:
                        top_zone_id = r[6]

                if r[9] is None:
                    continue
                else:
                    if r[9] > top_row:
                        top_row = r[9]

                if r[10] is None:
                    continue
                else:
                    if r[10] > top_column:
                        top_column = r[10]

        label = tk.Label(self,
                         text="Select Plot ID Number:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=8,
                   column=1,
                   columnspan=2)

        self.plot_spinbox = tk.Spinbox(self,
                                       from_=0,
                                       to=top_plot_id)
        self.plot_spinbox.grid(row=8,
                               column=3)

        label = tk.Label(self,
                         text="Or Select Zone, Row and Column below",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=8,
                   column=5,
                   columnspan=3)

        button = tk.Button(self,
                           text="Check Plot / Instant Add",
                           command=self.add_manual_set)
        button.grid(row=10,
                    column=3,
                    sticky='E')

        label = tk.Label(self,
                         text="Select Zone:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=9,
                   column=5,
                   columnspan=2)

        self.zone_combo = DropDown(self,
                                   zone_query,
                                   9,
                                   7,
                                   2,
                                   'W')

        label = tk.Label(self,
                         text="Select Row Number:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=10,
                   column=5,
                   columnspan=2)

        self.row_spinbox = tk.Spinbox(self,
                                      from_=0,
                                      to=top_row)
        self.row_spinbox.grid(row=10,
                              column=7)

        label = tk.Label(self,
                         text="Select Column Number:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=11,
                   column=5,
                   columnspan=2)

        self.col_spinbox = tk.Spinbox(self,
                                      from_=0,
                                      to=top_column)
        self.col_spinbox.grid(row=11,
                              column=7)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=13,
                    column=3,
                    sticky='E')

        self.new_plan = plan.Plan()

    def add(self):
        self.set_quantity = None
        self.fixed_location = None
        self.plant_id = None
        self.my_season_id = None
        self.plot_id = None
        self.set_type_id = None

        plant = self.plant_combo.selection
        set_type = self.set_type_combo.selection
        self.set_quantity = self.quantity_entry.get()

        self.plant_id = self.plant_combo.get_id(plant_name_query,
                                                plant)
        self.set_type_id = self.set_type_combo.get_id(set_type_query,
                                                      set_type)

        self.new_plant_set = plant_set.PlantSet()
        self.new_plant_set.add_new_plant_set(self.plant_id,
                                             self.set_type_id,
                                             self.set_quantity)

        self.new_plan.plant_set_list.append(self.new_plant_set)

        self.new_plan.display_plant_set_list()

        plant_string = (str(self.set_quantity) + " " + set_type
                        + " of " + plant + " added to Garden Plan")

        label = ttk.Label(self,
                          text=plant_string)
        label.grid(row=7,
                   column=1,
                   sticky='E')

    def complete(self):
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

            self.this_plot = plot.Plot()
            self.this_plot.set_plot_values(
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

            self.new_plan.plot_list.append(self.this_plot)

        self.new_plan.display_plot_list()
        self.new_plan.display_plant_set_list()

        self.new_plan.execute_plan()

        self.new_plan.display_plant_set_list()

    def add_manual_set(self):

        self.set_quantity = None
        self.fixed_location = None
        self.plant_id = None
        self.my_season_id = None
        self.set_plot_id = None
        self.set_type_id = None
        self.zone_id = None
        self.row = None
        self.column = None

        self.set_quantity = self.quantity_entry.get()
        self.set_plot_id = self.plot_spinbox.get()
        self.row = self.row_spinbox.get()
        self.column = self.col_spinbox.get()

        plant = self.plant_combo.selection
        self.plant_id = self.plant_combo.get_id(plant_name_query,
                                                plant)

        set_type = self.set_type_combo.selection
        self.set_type_id = self.set_type_combo.get_id(set_type_query,
                                                      set_type)
        set_season = self.season_combo.selection
        self.my_season_id = self.season_combo.get_id(seasons_query,
                                                     set_season)

        zone = self.zone_combo.selection
        self.zone_id = self.zone_combo.get_id(zone_query,
                                              zone)

        self.new_plant_set = plant_set.PlantSet()
        self.new_plant_set.add_new_plant_set(self.plant_id,
                                             self.set_type_id,
                                             self.set_quantity)

        print(self.my_season_id)
        print(self.set_plot_id)
        print(self.zone_id)
        print(self.row)
        print(self.column)

        this_manual_plan = plan.Plan()
        this_manual_plan.manual_plan(self.new_plant_set,
                                     self.my_season_id,
                                     self.set_plot_id,
                                     self.zone_id,
                                     self.row,
                                     self.column)

    def reset_plant_dropdown(self):
        self.plant_combo = DropDown(self,
                                    plant_name_query,
                                    3,
                                    2,
                                    2,
                                    'W')


class EditSetPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,
                         text="Edit Plant Set",
                         font=LARGE_FONT)
        label.grid(row=1,
                   column=2)

        label = tk.Label(self,
                         text=" ")
        label.grid(row=2,
                   column=1,
                   columnspan=5)

        self.set_default_values(controller)

    def set_default_values(self, controller):

        label = tk.Label(self,
                         text="Select Plant Name:")
        label.grid(row=3,
                   column=1,
                   columnspan=1)

        self.plant_combo = DropDown(self,
                                    planting_plan_query,
                                    3,
                                    2,
                                    2,
                                    'W')

        label = tk.Label(self,
                         text="Season:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=3,
                   column=4,
                   columnspan=1)

        self.season_combo = DropDown(self,
                                     seasons_query,
                                     3,
                                     5,
                                     1,
                                     'W')

        button = tk.Button(self,
                           text="Search",
                           command=self.import_plant_set,
                           width=10)
        button.grid(row=3,
                    column=6,
                    sticky='E')

        self.search_error = tk.Label(self)

        label = tk.Label(self,
                         text="Plant Set ID:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=4,
                   column=1,
                   columnspan=1)

        self.plant_set_id = 0

        label = tk.Label(self,
                         text=self.plant_set_id)
        label.grid(row=4,
                   column=2)

        label = tk.Label(self,
                         text="Set Type:")
        label.grid(row=4,
                   column=4)

        self.set_type_combo = DropDown(self,
                                       set_type_query,
                                       4,
                                       5,
                                       1,
                                       'W')

        label = tk.Label(self,
                         text="Quantity:")
        label.grid(row=4,
                   column=6)
        self.quantity_entry = tk.Entry(self,
                                       width=5)
        self.quantity_entry.grid(row=4,
                                 column=7)

        label = tk.Label(self,
                         text="Plot ID Number:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=5,
                   column=1,
                   columnspan=1)

        self.plot_id = '0'

        self.plot_entry = tk.Entry(self,
                                   width=5)
        self.plot_entry.grid(row=5,
                             column=2)
        self.plot_entry.insert(0, self.plot_id)

        label = tk.Label(self,
                         text=" ")
        label.grid(row=7,
                   column=1)

        label = (tk.Label
                 (self,
                  text="Plant Set Notes (Optional):"))
        label.grid(row=7,
                   column=2,
                   columnspan=2)

        self.set_notes_text = tk.Text(self,
                                      height=3,
                                      width=30)
        self.set_notes_text.grid(row=7,
                                 column=4,
                                 columnspan=2)

        label = tk.Label(self,
                         text="Date Planted:")
        label.grid(row=6,
                   column=6,
                   columnspan=2)
        self.date_planted_entry = tk.Entry(self,
                                           width=10)
        self.date_planted_entry.grid(row=6,
                                     column=8)

        label = tk.Label(self,
                         text="First Harvest Date (MM/DD/YY):")
        label.grid(row=7,
                   column=6,
                   columnspan=2)
        self.first_harvest_entry = tk.Entry(self,
                                            width=10)
        self.first_harvest_entry.grid(row=7,
                                      column=8)

        label = tk.Label(self,
                         text="Last Harvest Date (MM/DD/YY)")
        label.grid(row=8,
                   column=6,
                   columnspan=2)
        self.last_harvest_entry = tk.Entry(self,
                                           width=10)
        self.last_harvest_entry.grid(row=8,
                                     column=8)

        def select_radio():
            self.radio_selection = outcome_radio_entry.get()
            print(self.radio_selection)

        label = tk.Label(self,
                         text="Outcome:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=9,
                   column=5)

        outcome_radio_entry = tk.IntVar()
        self.radio_selection = None

        self.radio1 = tk.Radiobutton(self, text="Pending", variable=outcome_radio_entry, value=9, command=select_radio)
        self.radio1.grid(row=9,
                         column=6)

        self.radio2 = tk.Radiobutton(self, text="Success", variable=outcome_radio_entry, value=1, command=select_radio)
        self.radio2.grid(row=9,
                         column=7)

        self.radio3 = tk.Radiobutton(self, text="Failure", variable=outcome_radio_entry, value=0, command=select_radio)
        self.radio3.grid(row=9,
                         column=8)

        self.radio1.select()

        button = tk.Button(self,
                           text="Save Changes",
                           command=self.export_edited_set)
        button.grid(row=13,
                    column=3,
                    sticky='E')

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))

        button.grid(row=13,
                    column=7,
                    sticky='E')

        self.plant_name = None
        self.season_text = None
        # plant_set_id set further up

    def import_plant_set(self):

        self.saved_plant_set = plant_set.PlantSet()
        plant_selection = self.plant_combo.selection
        season_selection = self.season_combo.selection

        q_plant_set_id = self.saved_plant_set.import_plant_set(plant_selection,
                                                               season_selection)

        if q_plant_set_id is None:

            self.search_error = tk.Label(self,
                                         text="Plant Not Found")
            self.search_error.grid(row=3,
                                   column=7)
            print('not found')
        else:

            print(self.plant_set_id)

        if q_plant_set_id is not None:
            self.reset_values()
        else:
            self.set_default_values()

    def reset_values(self):

        # probably should change to a popup if not found above, and omit this
        self.search_error = tk.Label(self,
                                     text="                            ")
        self.search_error.grid(row=3,
                               column=7)

        label = tk.Label(self,
                         text=self.saved_plant_set.plant_set_id)
        label.grid(row=4,
                   column=2)

        self.set_type_combo.combo.set(self.saved_plant_set.set_type)

        self.quantity_entry.delete(0, 'end')
        self.quantity_entry.insert(0, self.saved_plant_set.set_quantity)

        self.plot_entry.delete(0, 'end')
        self.plot_entry.insert(0, self.saved_plant_set.plot_id)

        self.set_notes_text.delete(1.0, 'end')
        if self.saved_plant_set.plant_set_notes is not None:
            self.set_notes_text.insert(1.0, self.saved_plant_set.plant_set_notes)

        self.date_planted_entry.delete(0, 'end')
        if self.saved_plant_set.planted_date is not None:
            self.date_planted_entry.insert(0, self.saved_plant_set.planted_date)

        self.first_harvest_entry.delete(0, 'end')
        if self.saved_plant_set.first_harvest_date is not None:
            self.first_harvest_entry.insert(0, self.saved_plant_set.first_harvest_date)

        self.last_harvest_entry.delete(0, 'end')
        if self.saved_plant_set.last_harvest_date is not None:
            self.last_harvest_entry.insert(0, self.saved_plant_set.last_harvest_date)

        if self.saved_plant_set.outcome == 1:
            self.radio2.select()
        elif self.saved_plant_set.outcome == 0:
            self.radio3.select()
        else:
            self.radio1.select()

    def export_edited_set(self):

        plant = self.plant_combo.selection
        self.plant_id = self.plant_combo.get_id(plant_name_query,
                                                plant)

        set_season = self.season_combo.selection
        self.season_id = self.season_combo.get_id(seasons_query,
                                                  set_season)

        if self.season_id is None:
            this_connection = data_connection.Connection()  # connect to server
            cursor = this_connection.connection.cursor()  # set connection cursor
            cursor.execute(seasons_query)
            records = cursor.fetchall()
            for r in records:
                if self.saved_plant_set.season_text == r[1]:
                    self.season_id = r[0]

        self.set_quantity = self.quantity_entry.get()

        self.plot_id = self.plot_entry.get()

        set_type = self.set_type_combo.selection
        self.set_type_id = self.set_type_combo.get_id(set_type_query,
                                                      set_type)
        if self.set_type_id is None:
            this_connection = data_connection.Connection()  # connect to server
            cursor = this_connection.connection.cursor()  # set connection cursor
            cursor.execute(set_type_query)
            records = cursor.fetchall()
            for r in records:
                if self.saved_plant_set.set_type == r[1]:
                    self.set_type_id = r[0]

        self.set_notes = self.set_notes_text.get(1.0, 'end')
        self.planted_date = self.date_planted_entry.get()
        if self.planted_date == "":
            self.planted_date = None
        self.first_harvest_date = self.first_harvest_entry.get()
        if self.first_harvest_date == "":
            self.first_harvest_date = None
        self.last_harvest_date = self.last_harvest_entry.get()
        if self.last_harvest_date == "":
            self.last_harvest_date = None

        if self.radio_selection is None:
            self.outcome = self.saved_plant_set.outcome

        elif self.radio_selection == 9:
            self.outcome = None
        else:
            self.outcome = self.radio_selection

        self.updated_set = plant_set.PlantSet()

        print('hello1')

        self.updated_set.export_updated_set(  # seems that season ID, plot ID, plant set ID is None
            self.saved_plant_set.plant_set_id,
            self.set_quantity,
            self.planted_date,
            self.first_harvest_date,
            self.last_harvest_date,
            self.outcome,
            self.plant_id,
            self.season_id,
            self.plot_id,
            self.set_type_id,
            self.set_notes)


class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = (tk.Label
                 (self,
                  text="Setup Menu",
                  font=LARGE_FONT))
        label.grid(row=1,
                   column=2,
                   columnspan=4)

        label = (tk.Label
                 (self,
                  text="Configure Settings",
                  justify=tk.LEFT,
                  anchor='w'))
        label.grid(row=2,
                   column=1,
                   columnspan=2)

        label = tk.Label(self,
                         text=" ",
                         width='5')
        label.grid(row=3,
                   column=1)

        button = tk.Button(self,
                           text="Configure Zones",
                           command=lambda: controller.show_frame(ConfigureZonesPage))
        button.grid(row=3,
                    column=2,
                    sticky='W')

        label = tk.Label(self,
                         text=" ",
                         width='5')
        label.grid(row=3,
                   column=3)

        button = tk.Button(self,
                           text="Configure Plots",
                           command=lambda: controller.show_frame(AddPlotsPage))
        button.grid(row=3,
                    column=4,
                    sticky='W')

        label = tk.Label(self,
                         text=" ",
                         width='5')
        label.grid(row=4,
                   column=3)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=6,
                    column=1,
                    columnspan=8,
                    sticky='S')


class ConfigureZonesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = (tk.Label
                 (self,
                  text="New / Edit Zone",
                  font=LARGE_FONT))
        label.grid(row=1,
                   column=2,
                   columnspan=4)

        label = (tk.Label
                 (self,
                  text=""))
        label.grid(row=2,
                   column=2)

        label = (tk.Label
                 (self,
                  text='A "plot" is a space where a single plant'
                       ' or plant set can be planted.'))
        label.grid(row=3,
                   column=1,
                   columnspan=8)
        label = (tk.Label
                 (self,
                  text='A "Zone" is a group of contiguous plots,'
                       ' such as a designated garden area or raised bed'))
        label.grid(row=4,
                   column=1,
                   columnspan=8)

        label = (tk.Label
                 (self,
                  text=""))
        label.grid(row=5,
                   column=2)

        label = (tk.Label
                 (self,
                  text='Please enter a unique name for your zone: '))
        label.grid(row=6,
                   column=1,
                   columnspan=4)

        label = (tk.Label
                 (self,
                  text='Ex. "Large Garden, Blue Flowerpot 1'))
        label.grid(row=7,
                   column=1,
                   columnspan=5)

        self.zone_name_entry = tk.Entry(self,
                                        justify=tk.LEFT,
                                        width=40,
                                        )
        self.zone_name_entry.grid(row=6,
                                  column=5,
                                  columnspan=3)
        label = (tk.Label
                 (self,
                  text=""))
        label.grid(row=8,
                   column=2)

        label = (tk.Label
                 (self,
                  text="Number of rows of plots in this zone:"))
        label.grid(row=9,
                   column=1,
                   columnspan=4)

        self.zone_rows_entry = tk.Entry(self,
                                        justify=tk.LEFT,
                                        width=5)
        self.zone_rows_entry.grid(row=9,
                                  column=5)

        label = (tk.Label
                 (self,
                  text="Number of columns of plots in this zone:"))
        label.grid(row=10,
                   column=1,
                   columnspan=4)

        self.zone_columns_entry = tk.Entry(self,
                                           justify=tk.LEFT,
                                           width=5)
        self.zone_columns_entry.grid(row=10,
                                     column=5)

        label = (tk.Label
                 (self,
                  text=""))
        label.grid(row=11,
                   column=2)

        label = (tk.Label
                 (self,
                  text="Zone Notes (Optional):"))
        label.grid(row=12,
                   column=1,
                   columnspan=2)

        self.zone_notes_text = tk.Text(self,
                                       height=3,
                                       width=30)
        self.zone_notes_text.grid(row=12,
                                  column=3,
                                  columnspan=4)

        label = (tk.Label
                 (self,
                  text=""))
        label.grid(row=13,
                   column=2)

        button = tk.Button(self, text="Add Zone",
                           command=self.add_new_zone)
        button.grid(row=14,
                    column=4)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=14,
                    column=6,
                    sticky='E')

    def add_new_zone(self):
        self.zone_rows = None
        self.zone_columns = None
        self.zone_notes = None  # in case left blank

        self.zone_name = self.zone_name_entry.get()
        self.zone_rows = int(self.zone_rows_entry.get())
        self.zone_columns = int(self.zone_columns_entry.get())
        self.zone_notes = self.zone_notes_text.get(1.0, tk.END)

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        (cursor.execute
         (add_zone_query + ' ?, ?, ?, ?',
          [self.zone_name,
           self.zone_rows,
           self.zone_columns,
           self.zone_notes
           ]))

        cursor.commit()  # finalize entry into table

        print('Finished Inserting the following Zone: ' + self.zone_name)  # confirmation

        this_connection.end_connection()


class AddPlotsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = (tk.Label
                 (self,
                  text="Add New Plots",
                  font=LARGE_FONT))
        label.grid(row=1,
                   column=2,
                   columnspan=4)

        label = (tk.Label
                 (self,
                  text=""))
        label.grid(row=2,
                   column=2)

        label = (tk.Label
                 (self,
                  text="Please select a Zone:"))
        label.grid(row=3,
                   column=1,
                   columnspan=2)

        self.zone_combo = DropDown(self,
                                   zone_query,
                                   3,
                                   3,
                                   2,
                                   'W')

        label = tk.Label(self,
                         text="Refresh the list if new zones have been added:")
        label.grid(row=3,
                   column=5,
                   columnspan=3)

        button = tk.Button(self,
                           text="Refresh Zones",
                           command=self.reset_zone_dropdown)
        button.grid(row=3,
                    column=9,
                    sticky='E')

        label = (tk.Label
                 (self,
                  text="Number of rows of identical plots to add:"))
        label.grid(row=4,
                   column=1,
                   columnspan=3)

        self.quantity_rows_entry = tk.Entry(self,
                                            width=5)
        self.quantity_rows_entry.grid(row=4,
                                      column=4)

        label = (tk.Label
                 (self,
                  text="Number of columns of identical plots to add:"))
        label.grid(row=5,
                   column=1,
                   columnspan=3)

        self.quantity_columns_entry = tk.Entry(self,
                                               width=5)
        self.quantity_columns_entry.grid(row=5,
                                         column=4)

        label = (tk.Label
                 (self,
                  text="Size of each Plot:",
                  anchor='e',
                  justify=tk.RIGHT))
        label.grid(row=6,
                   column=1)

        self.plot_size_entry = tk.Entry(self,
                                        width=5,
                                        justify=tk.LEFT)
        self.plot_size_entry.grid(row=6,
                                  column=2)

        label = (tk.Label
                 (self,
                  text="Unit of Measurement:"))
        label.grid(row=6,
                   column=3,
                   columnspan=2)

        self.measurement_combo = DropDown(self,
                                          measurement_unit_query,
                                          6,
                                          5,
                                          2,
                                          'W')

        label = (tk.Label
                 (self,
                  text=""))
        label.grid(row=7,
                   column=1)

        self.is_container = tk.IntVar()
        self.is_container_checkbox \
            = (tk.Checkbutton(self,
                              text="Is this plot a container (solid bottom)?",
                              variable=self.is_container,
                              onvalue=1,
                              offvalue=0,
                              width=40,
                              justify=tk.LEFT,
                              anchor='w'))
        self.is_container_checkbox.grid(row=7,
                                        column=2,
                                        columnspan=3)

        label = (tk.Label
                 (self,
                  text="If container, container depth in inches:"))
        label.grid(row=8,
                   column=3,
                   columnspan=3)

        self.container_depth_entry = tk.Entry(self,
                                              width=5)
        self.container_depth_entry.grid(row=8,
                                        column=6)

        label = (tk.Label
                 (self,
                  text="Sun Level of Plot(s):"))
        label.grid(row=9,
                   column=1,
                   columnspan=2)

        self.sun_combo = DropDown(self,
                                  sun_query,
                                  9,
                                  3,
                                  2,
                                  'W')

        label = (tk.Label
                 (self,
                  text="Soil Moisture Level of Plot(s):"))
        label.grid(row=9,
                   column=5,
                   columnspan=2)

        self.soil_moisture_combo = DropDown(self,
                                            soil_moisture_query,
                                            9,
                                            7,
                                            2,
                                            'W')

        button = tk.Button(self, text="Add Plots",
                           command=self.add_new_plots)
        button.grid(row=12,
                    column=4)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=12,
                    column=6,
                    sticky='E')

    def add_new_plots(self):
        self.total_rows = None
        self.total_columns = None
        self.plot_size = None
        self.measurement_unit_id = None
        self.container = None
        self.container_depth = None
        self.zone_id = None
        self.sun_id = None
        self.soil_moisture_id = None
        self.plot_nitrogen_level = 3
        self.plot_active = True

        total_rows = int(self.quantity_rows_entry.get())
        total_columns = int(self.quantity_columns_entry.get())
        self.total_plots = total_rows * total_columns
        self.plot_size = int(self.plot_size_entry.get())
        measurement_unit_text = self.measurement_combo.selection
        self.measurement_unit_id = \
            int(self.measurement_combo.get_id(measurement_unit_query,
                                              measurement_unit_text))
        self.container = bool(self.is_container.get())
        if self.container:
            self.container_depth = int(self.container_depth_entry.get())
        zone_text = self.zone_combo.selection
        self.zone_id = int(self.zone_combo.get_id(zone_query,
                                                  zone_text))
        sun_text = self.sun_combo.selection
        self.sun_id = int(self.sun_combo.get_id(sun_query,
                                                sun_text))
        soil_moisture_text = self.soil_moisture_combo.selection
        self.soil_moisture_id = int(self.soil_moisture_combo.get_id(soil_moisture_query,
                                                                    soil_moisture_text))

        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        last_record_id = None
        plot_id = None
        record_zone_id = None
        last_row_zone = None

        cursor.execute(plot_data_query)
        records = cursor.fetchall()
        for r in records:
            last_record_id = r[0]
            record_zone_id = r[6]
            if last_record_id is None:
                break
            elif record_zone_id == self.zone_id:
                last_row_zone = r[9]
            else:
                continue

        if last_record_id is None:
            plot_id = 1
            row = 1
        else:
            plot_id = last_record_id + 1
            if last_row_zone is None:
                row = 1
            else:
                row = last_row_zone + 1

        column = 1
        self.new_plot_list = []

        for id in range(self.total_plots):
            self.new_plot = plot.Plot()

            if column > total_columns:
                row = row + 1
                column = 1

            self.plot_id = plot_id
            self.plot_row = row
            self.plot_column = column
            column = column + 1

            self.new_plot.set_plot_values(
                self.plot_id,
                self.plot_size,
                self.measurement_unit_id,
                self.container,
                self.container_depth,
                self.plot_nitrogen_level,
                self.zone_id,
                self.sun_id,
                self.soil_moisture_id,
                self.plot_row,
                self.plot_column,
                self.plot_active)

            self.new_plot_list.append(self.new_plot)

            plot_id = plot_id + 1

        for np in self.new_plot_list:
            np.display_plot()
            np.export_plot(np.plot_id,
                           np.plot_size,
                           np.measurement_unit_id,
                           np.is_container,
                           np.container_depth,
                           np.zone_id,
                           np.sun_id,
                           np.soil_moisture_id,
                           np.plot_row,
                           np.plot_column)

        this_connection.end_connection()

    def reset_zone_dropdown(self):
        self.zone_combo = DropDown(self,
                                   zone_query,
                                   3,
                                   3,
                                   2,
                                   'W')


class DisplayPlan(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self,
                         text="Current Garden Plan",
                         font=LARGE_FONT)
        label.grid(row=1,
                   column=1,
                   columnspan=8)

        label = tk.Label(self,
                         text=" ",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=2,
                   column=1)

        label = tk.Label(self,
                         text="Select your Season:",
                         justify=tk.RIGHT,
                         anchor='e')
        label.grid(row=3,
                   column=1,
                   columnspan=2)

        self.season_combo = DropDown(self,
                                     seasons_query,
                                     3,
                                     3,
                                     2,
                                     'W')

        tk.Label(self,
                 text=" ").grid(row=3,
                                column=5)

        button = tk.Button(self, text="View Plan for Season",
                           command=self.view_season_plan)
        button.grid(row=3,
                    column=6)

        tk.Label(self,
                 text=" ").grid(row=3,
                                column=7)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))

        button.grid(row=3,
                    column=8)

    def reset_grid(self):
        for label in self.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def view_season_plan(self):

        self.reset_grid()

        tk.Label(self,
                 text="Current Garden Plan",
                 font=LARGE_FONT).grid(row=1,
                                       column=1,
                                       columnspan=8)

        tk.Label(self,
                 text=" ",
                 justify=tk.RIGHT,
                 anchor='e').grid(row=2,
                                  column=1)

        self.set_season_id()
        self.query_grid(display_grid_query, self.season_id)

    def set_season_id(self):
        season = self.season_combo.selection

        if season is None:
            tk.Label(self,
                     text="No Season Selected").grid(row=4,
                                                     column=2)
        self.season_id = self.season_combo.get_id(seasons_query, season)

    def query_grid(self, display_grid_query, season_id):
        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(display_grid_query + ' ?', [season_id])

        zone = ''
        max_row = 0
        last_row = 6
        max_column = 0

        tk.Label(self, text=" ").grid(column=1,
                                      row=4)

        for row_number, data_row in enumerate(cursor):  # query is sorted by zones already
            current_zone = data_row[0]
            current_row = data_row[2]
            current_column = data_row[3] + 1
            current_plant = data_row[5]

            print(max_row)
            print(max_column)
            print(last_row)
            print(current_zone)

            if zone == '':
                tk.Label(self, text=str(current_zone)).grid(column=1, row=last_row)
            elif zone != current_zone:
                last_row = last_row + max_row + 1
                tk.Label(self, text=' ').grid(column=1, row=last_row)
                last_row = last_row + 1
                tk.Label(self, text=str(current_zone)).grid(column=1, row=last_row)
                max_row = 0
            else:
                if current_row > max_row:
                    max_row = current_row

            tk.Label(self, text=str(current_plant)).grid(column=current_column, row=current_row + last_row)
            tk.Label(self, text='Row ' + str(current_row)).grid(column=1, row=current_row + last_row)

            if current_column >= max_column:
                max_column = current_column

            zone = current_zone

        for column in range(1, max_column):
            tk.Label(self, text='Column ' + str(column)).grid(column=column + 1, row=5)

        this_connection.end_connection()


class PlantingPlanReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self,
                         text="Current Garden Plan",
                         font=LARGE_FONT)
        label.grid(row=1,
                   column=1,
                   columnspan=8)

        label = tk.Label(self,
                         text="Click Here for Current Plan: ",
                         anchor='e',
                         justify=tk.RIGHT)
        label.grid(row=1,
                   column=9,
                   columnspan=1)

        button = tk.Button(self,
                           text="Current Plan",
                           anchor='w',
                           justify=tk.LEFT,
                           command=lambda: self.query_plan(controller))
        button.grid(row=1,
                    column=10)

        label = tk.Label(self,
                         text=" ",
                         font=LARGE_FONT)
        label.grid(row=2,
                   column=2)

        label = tk.Label(self,
                         text="Plant")
        label.grid(row=3,
                   column=2)

        label = tk.Label(self,
                         text="Season")
        label.grid(row=3,
                   column=3)

        label = tk.Label(self,
                         text="Zone")
        label.grid(row=3,
                   column=4)

        label = tk.Label(self,
                         text="Plot Number")
        label.grid(row=3,
                   column=5)

        label = tk.Label(self,
                         text="Space per Seed Pack")
        label.grid(row=3,
                   column=6)

        label = tk.Label(self,
                         text="Space per Seedling")
        label.grid(row=3,
                   column=7)

        label = tk.Label(self,
                         text="Depth to Plant Seeds")
        label.grid(row=3,
                   column=8)

        label = tk.Label(self,
                         text="Watering Frequency")
        label.grid(row=3,
                   column=9)

        label = tk.Label(self,
                         text="Days to Harvest")
        label.grid(row=3,
                   column=10)

        self.query_plan(controller)

    def query_plan(self, controller):
        this_connection = data_connection.Connection()
        cursor = this_connection.connection.cursor()

        cursor.execute(planting_plan_query)

        for row_number, row in enumerate(cursor, 4):
            tk.Label(self, text=str(row[1])).grid(column=2, row=row_number)
            tk.Label(self, text=str(row[2])).grid(column=3, row=row_number)
            tk.Label(self, text=str(row[3])).grid(column=4, row=row_number)
            tk.Label(self, text=str(row[4])).grid(column=5, row=row_number)
            tk.Label(self, text=str(row[5]) + ' inches').grid(column=6, row=row_number)
            tk.Label(self, text=str(row[6]) + ' inches').grid(column=7, row=row_number)
            tk.Label(self, text=str(row[7]) + ' inches').grid(column=8, row=row_number)
            tk.Label(self, text=str(row[8])).grid(column=9, row=row_number)
            tk.Label(self, text=str(row[9])).grid(column=10, row=row_number)

        this_connection.end_connection()

        label = tk.Label(self,
                         text=" ")
        label.grid(row=row_number + 1,
                   column=2)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=row_number + 2,
                    column=8)


app = Window()
app.mainloop()
