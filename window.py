import tkinter as tk  #see notes below on what needs fixing to add plant
import os
from tkinter import ttk
import data_connection  # manages connection to server
import plan
import plant
import plant_set
import plot

# works as of 9:37 AM 6/16

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

logo_file = "Logo.png"
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
                  DisplayPlants,
                  GardenPlanPage,
                  SetupPage,
                  ConfigureZonesPage,
                  ConfigurePlotsPage):
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
                   column=2)

        button = tk.Button(self,
                           width=40,
                           text="Add Plant",
                           command=lambda: controller.show_frame(AddPlantPage))
        button.grid(row=2,
                    column=1,
                    sticky='W')

        button = tk.Button(self,
                           width=40,
                           text="My Plants",
                           command=lambda: controller.show_frame(DisplayPlants))
        button.grid(row=2, column=2, sticky='E')

        button = tk.Button(self,
                           width=40,
                           text="Add Garden Plan",
                           command=lambda: controller.show_frame(GardenPlanPage))
        button.grid(row=2,
                    column=3,
                    sticky='E')

        button = tk.Button(self,
                           width=40,
                           text="Setup",
                           command=lambda: controller.show_frame(SetupPage))
        button.grid(row=3,
                    column=2,
                    sticky='E')



        button = tk.Button(self,
                           width=40,
                           text="Exit",
                           command=lambda: controller.close_window())
        button.grid(row=3,
                    column=3,
                    sticky='E')

        for child in self.winfo_children():
            child.grid_configure(padx=10,
                                 pady=10)


class AddPlantPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = (tk.Label
                 (self,
                  text="Add / Edit Plant",
                  font=LARGE_FONT))
        label.grid(row=1,
                   column=2,
                   columnspan=4)

        label = tk.Label(self,
                         text="Plant Name:",
                         justify=tk.LEFT,
                         anchor='w'
                         )
        label.grid(row=2,
                   column=1)
        self.plant_name_entry = tk.Entry(self,
                                         justify=tk.LEFT,
                                         width=40,
                                         )
        self.plant_name_entry.grid(row=2,
                                   column=2,
                                   columnspan=2)

        self.always_include = tk.IntVar()
        self.always_include_checkbox = (tk.Checkbutton(self,
                                               text="Always Include?",
                                               variable=self.always_include,
                                               onvalue=1,
                                               offvalue=0,
                                               width=20,
                                               justify=tk.LEFT,
                                               anchor='w'))
        self.always_include_checkbox.grid(row=2,
                                  column=4)


        self.plant_spring = tk.IntVar()
        self.spring_checkbox = (tk.Checkbutton(self,
                                               text="Plant in Spring",
                                               variable=self.plant_spring,
                                               onvalue=1,
                                               offvalue=0,
                                               width=20,
                                               justify=tk.LEFT,
                                               anchor='w'))
        self.spring_checkbox.grid(row=2,
                                  column=5)

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
                                column=5)

        label = tk.Label(self,
                         text="Days to Harvest:",
                         anchor='e',
                         justify=tk.RIGHT)
        label.grid(row=2,
                   column=6)

        self.days_to_harvest_entry = tk.Entry(self,
                     width=5,
                     justify=tk.LEFT)
        self.days_to_harvest_entry.grid(row=2,
                                        column=7)

        label = tk.Label(self,
                         text="Crop Rotation Group:")
        label.grid(row=4, column=1)
        self.crop_group_combo = DropDown(self,
                                         crop_group_query,
                                         4,
                                         2,
                                         1,
                                         'W')

        label = tk.Label(self,
                         text="Frost Tolerance:")
        label.grid(row=4,
                   column=3)
        self.frost_tolerance_combo = DropDown(self,
                                              frost_tolerance_query,
                                              4,
                                              4,
                                              1,
                                              'W')

        label = tk.Label(self,
                         text="Environment Requirements",
                         justify=tk.LEFT,
                         anchor='w')
        label.grid(row=5,
                   column=1,
                   columnspan=2,
                   sticky='W')

        label = tk.Label(self,
                         text="Sun:")
        label.grid(row=6,
                   column=1)
        self.sun_combo = DropDown(self,
                                  sun_query,
                                  6,
                                  2,
                                  1,
                                  'W')

        label = tk.Label(self,
                         text="Soil Moisture:")
        label.grid(row=6,
                   column=3)
        self.soil_moisture_combo = DropDown(self,
                                            soil_moisture_query,
                                            6,
                                            4,
                                            1,
                                            'W')

        label = tk.Label(self,
                         text="Watering:")
        label.grid(row=6,
                   column=5,
                   columnspan=1)
        self.watering_requirement_combo = DropDown(self,
                                                   watering_requirement_query,
                                                   6,
                                                   6,
                                                   1,
                                                   'W')

        label = tk.Label(self,
                         text="Spacing Requirements",
                         justify=tk.LEFT,
                         anchor='w')
        label.grid(row=7,
                   column=1,
                   columnspan=2,
                   sticky='W')


        label = tk.Label(self,
                         text="Space per Seedling, in inches:",
                         anchor='w',
                         justify=tk.RIGHT)
        label.grid(row=8,
                   column=1)

        self.space_per_seedling_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT)
        self.space_per_seedling_entry.grid(row=8,
                                        column=2)

        label = tk.Label(self,
                         text="Space per Seed Pack, in inches:",
                         anchor='w',
                         justify=tk.RIGHT)
        label.grid(row=8,
                   column=3)

        self.space_per_seedpack_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT)
        self.space_per_seedpack_entry.grid(row=8,
                                        column=4)

        label = tk.Label(self,
                         text="Depth per Plant, in inches:",
                         anchor='w',
                         justify=tk.RIGHT)
        label.grid(row=8,
                   column=5)

        self.depth_per_plant_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT)
        self.depth_per_plant_entry.grid(row=8,
                                        column=6)

        label = tk.Label(self,
                         text="Depth to Plant Seeds, inches, 2 decimals ok:",
                         anchor='w',
                         justify=tk.RIGHT)
        label.grid(row=8,
                   column=7)

        self.depth_for_seeds_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT)
        self.depth_for_seeds_entry.grid(row=8,
                                        column=8)

        label = tk.Label(self,
                         text=" ")
        label.grid(row=9,
                   column=5)

        self.new_plant = plant.Plant()

        button = tk.Button(self, text="Add Plant",
                           command=self.add_new_plant)
        button.grid(row=10,
                    column=5)

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=10,
                    column=6)

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
            self.crop_group_combo.get_id(crop_group_query,
                                         crop_group_text)
        sun_id_text = self.sun_combo.selection
        self.sun_id = self.sun_combo.get_id(sun_query, sun_id_text)
        soil_moisture_text = self.soil_moisture_combo.selection
        self.soil_moisture_id = \
            self.soil_moisture_combo.get_id(soil_moisture_query,
                                            soil_moisture_text)
        frost_tolerance_text = self.frost_tolerance_combo.selection
        self.frost_tolerance_id = \
            self.frost_tolerance_combo.get_id(frost_tolerance_query,
                                              frost_tolerance_text)
        self.space_required_seeds = self.space_per_seedpack_entry.get()
        self.space_required_seedling = self.space_per_seedling_entry.get()
        self.depth_requirement = self.depth_per_plant_entry.get()
        self.depth_to_plant_seeds = self.depth_for_seeds_entry.get()
        watering_requirement_text = self.watering_requirement_combo.selection
        self.watering_requirement_id = \
            self.watering_requirement_combo.get_id(watering_requirement_query,
                                                   watering_requirement_text)

        self.plant_in_spring = self.plant_spring.get()
        self.plant_in_fall = self.plant_fall.get()
        self.days_to_harvest = self.days_to_harvest_entry.get()

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
                   column=2)
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
                           text="Add to Plan",
                           command=self.add)
        button.grid(row=4,
                    column=5,
                    sticky='E')

        button = tk.Button(self,
                           text="Complete",
                           command=self.complete)
        button.grid(row=5,
                    column=5,
                    sticky='E')

        button = tk.Button(self,
                           text="Exit to Main",
                           command=lambda: controller.show_frame(StartPage))
        button.grid(row=6,
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
            plot_active = r[9]

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
                plot_active)

            self.new_plan.plot_list.append(self.this_plot)

        self.new_plan.display_plot_list()
        self.new_plan.display_plant_set_list()

        self.new_plan.execute_plan()

        self.new_plan.display_plant_set_list()

    def reset_plant_dropdown(self):
        self.plant_combo = DropDown(self,
                                    plant_name_query,
                                    3,
                                    2,
                                    2,
                                    'W')


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
                           command=lambda: controller.show_frame(StartPage))
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


class ConfigurePlotsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = (tk.Label
                 (self,
                  text="New / Edit Plot",
                  font=LARGE_FONT))
        label.grid(row=1,
                   column=2,
                   columnspan=4)





app = Window()
app.mainloop()
