import tkinter as tk
import os
from tkinter import ttk
import data_connection  # manages connection to server
import my_season
import plan
import plant
import plant_set
import plot
import export_query
import planting_year
from datetime import date

LARGE_FONT = ("Helvetica", 16, 'bold')
MEDIUM_FONT = ("Helvetica", 14)

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
measurement_unit_query = 'RetrieveMeasurementUnitData'
seasons_query = 'RetrieveMySeasonData'

# SQL queries for reports and data entry
add_zone_query = 'AddZone'
plant_detail_query = 'QueryAllPlantsSetupDetail'
planting_plan_query = 'QueryPlantingPlan'
outcome_detail_query = 'QueryOutcomeDetail'
outcome_summary_query = 'QueryOutcomeSummary'
display_grid_query = 'QueryPlotGrid'

# SQL query to handle year changeover
year_data_query = 'QueryYearData'


# class to manage all dropdown lists

class DropDown:
    def __init__(self,
                 parent,
                 query_name,
                 row,
                 column,
                 columnspan,
                 sticky):
        try:
            self.this_connection = data_connection.Connection()
            self.cursor = self.this_connection.connection.cursor()

            self.drop_down_list = []
            self.selection = None
            self.id = None

            self.cursor.execute(query_name)
            records = self.cursor.fetchall()
            for r in records:
                drop_down_value = r[1]
                if drop_down_value in self.drop_down_list:
                    continue
                else:
                    self.drop_down_list.append(drop_down_value)

            self.combo = ttk.Combobox(parent,
                                      values=self.drop_down_list)
            self.combo.grid(row=row,
                            column=column,
                            columnspan=columnspan,
                            sticky=sticky)
            self.combo.set('Select Value')
            self.combo.bind('<<ComboboxSelected>>',
                            self.get_value)
        except:
            print("no connection dropdown")

    def get_value(self,
                  event):
        print(self.combo.get())
        self.selection = self.combo.get()
        print(self.selection)

    def get_id(self,
               query_name,
               value):
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

    def __init__(self,
                 *args,
                 **kwargs):
        tk.Tk.__init__(self,
                       *args,
                       **kwargs)
        container = tk.Frame(self)
        self.title("Let it Grow Garden Planner")

        icon_file = "Icon.png"  # icon in the top left corner
        img = tk.PhotoImage(file=icon_file)
        self.iconphoto(False, img)

        container.pack(side="top",
                       fill="both",
                       expand=True)

        container.grid_rowconfigure(0,
                                    weight=1)
        container.grid_columnconfigure(0,
                                       weight=1)

        self.geometry("1000x400")

        self.frames = {}

        for F in (StartPage,
                  AddPlantPage,
                  ReportsMenu,
                  EditSetPage,
                  DisplayPlan,
                  GardenPlanPage,
                  SetupPage,
                  AddZonesPage,
                  AddPlotsPage,
                  EditPlotPage,
                  AddSeasonPage,
                  EditSeasonPage,
                  PlantingPlanReport,
                  PlantsDetailReport,
                  OutcomeDetailReport,
                  OutcomeSummaryReport,
                  CompleteYearPage):
            frame = F(container,
                      self)

            self.frames[F] = frame

            frame.configure(background='white')

            frame.grid(row=0,
                       column=0,
                       sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def close_window(self):
        exit()

    def close_popup(self, top):
        top.destroy()

    def open_popup(self, controller, message):
        top = tk.Toplevel(self)
        top.geometry("500x250")
        top.configure(bg='white')

        top.title("Notification")

        icon_file = "Icon.png"  # icon in the top left corner
        img = tk.PhotoImage(file=icon_file)
        top.iconphoto(False, img)

        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=1,
                                  column=1,
                                  sticky="nsew")
        tk.Label(top,
                 text=message,
                 justify=tk.CENTER,
                 anchor="center",
                 bg='white').grid(row=2,
                                  column=1,
                                  columnspan=3,
                                  sticky="nsew")
        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=3,
                                  column=1,
                                  sticky="nsew")
        tk.Button(top,
                  width=10,
                  text="OK",
                  bg='dimgrey',
                  fg='white',
                  command=lambda: controller.close_popup(top)).grid(row=4,
                                                                    column=2,
                                                                    sticky='E')


# Landing Page for Program / Main Menu
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # open a window

        # start page logo file name
        logo_file = "WelcomeLogo.png"

        # set file path for logo file location
        path = os.path.abspath(__file__)
        logo_dir = os.path.dirname(path)
        logo_path = os.path.join(logo_dir, logo_file)

        # display logo
        logo = tk.PhotoImage(file=logo_path)
        label = tk.Label(image=logo)
        label.image = logo

        tk.Label(self,
                 image=label.image, border=0).grid(row=1,
                                                   column=1,
                                                   columnspan=3)

        tk.Label(self,
                 text="Welcome! Please make a selection below.",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=2,
                                  column=1,
                                  columnspan=3)

        # Buttons to navigate to subpages and submenus

        tk.Button(self,
                  width=25,
                  text="Garden Setup & Maintenance",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(SetupPage)).grid(row=3,
                                                                         column=1,
                                                                         sticky='E')
        tk.Button(self,
                  width=25,
                  text="Add Plant",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(AddPlantPage)).grid(row=3,
                                                                            column=2,
                                                                            sticky='W')
        tk.Button(self,
                  width=25,
                  text="Complete Year",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(CompleteYearPage)).grid(row=4,
                                                                                column=1,
                                                                                sticky='E')
        tk.Button(self,
                  width=25,
                  text="Reports",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(ReportsMenu)).grid(row=4,
                                                                           column=2,
                                                                           sticky='E')
        tk.Button(self,
                  width=25,
                  text="Start Garden Plan",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(GardenPlanPage)).grid(row=3,
                                                                              column=3,
                                                                              sticky='E')
        tk.Button(self,
                  width=25,
                  text="View Garden Plan",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(DisplayPlan)).grid(row=4,
                                                                           column=3,
                                                                           sticky='E')
        tk.Button(self,
                  width=25,
                  text="Exit",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.close_window()).grid(row=5,
                                                                  column=2,
                                                                  sticky='E')

        for child in self.winfo_children():
            child.grid_configure(padx=10,
                                 pady=10)


# class to add a new plant to the master list

class AddPlantPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # launch window

        tk.Label(self,
                 text="Add Plant",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Label(self,
                 text="Plant Name:",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        self.plant_name_entry = tk.Entry(self,
                                         justify=tk.LEFT,
                                         width=40,
                                         bg='white',
                                         relief='solid')
        self.plant_name_entry.grid(row=3,
                                   column=3,
                                   columnspan=2)

        self.plant_spring = tk.IntVar()
        self.spring_checkbox = (tk.Checkbutton(self,
                                               text="Plant in Spring",
                                               variable=self.plant_spring,
                                               onvalue=1,
                                               offvalue=0,
                                               width=20,
                                               justify=tk.LEFT,
                                               anchor='w',
                                               bg='white'))
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
                                             anchor='w',
                                             bg='white'))
        self.fall_checkbox.grid(row=3,
                                column=7)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)

        tk.Label(self,
                 text="Crop Rotation Group:",
                 bg='white').grid(row=5,
                                  column=1,
                                  columnspan=2)

        self.crop_group_combo = DropDown(self,
                                         crop_group_query,
                                         5,
                                         3,
                                         1,
                                         'W')

        tk.Label(self,
                 text="Frost Tolerance:",
                 bg='white').grid(row=5,
                                  column=4,
                                  columnspan=2)

        self.frost_tolerance_combo = DropDown(self,
                                              frost_tolerance_query,
                                              5,
                                              6,
                                              1,
                                              'W')

        tk.Label(self,
                 text="",
                 bg='white').grid(row=6,
                                  column=1)

        tk.Label(self,
                 text="Sun Required:",
                 bg='white').grid(row=7,
                                  column=1,
                                  columnspan=2)

        self.sun_combo = DropDown(self,
                                  sun_query,
                                  7,
                                  3,
                                  1,
                                  'W')

        tk.Label(self,
                 text="Soil Moisture Required:",
                 bg='white').grid(row=7,
                                  column=4,
                                  columnspan=2)

        self.soil_moisture_combo = DropDown(self,
                                            soil_moisture_query,
                                            7,
                                            6,
                                            1,
                                            'W')

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=8,
                                  column=1)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=9,
                                  column=1)

        tk.Label(self,
                 text="Space per Seedling, in inches:",
                 anchor='e',
                 justify=tk.RIGHT,
                 bg='white').grid(row=9,
                                  column=2,
                                  columnspan=2)

        self.space_per_seedling_entry = tk.Entry(self,
                                                 width=5,
                                                 justify=tk.LEFT,
                                                 bg='white',
                                              relief='solid')
        self.space_per_seedling_entry.grid(row=9,
                                           column=4)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=10,
                                  column=1)

        tk.Label(self,
                 text="Space per Seed Pack, in inches:",
                 anchor='e',
                 justify=tk.RIGHT,
                 bg='white').grid(row=10,
                                  column=2,
                                  columnspan=2)

        self.space_per_seedpack_entry = tk.Entry(self,
                                                 width=5,
                                                 justify=tk.LEFT,
                                                 bg='white',
                                              relief='solid')
        self.space_per_seedpack_entry.grid(row=10,
                                           column=4)

        tk.Label(self,
                 text="Depth Required per Plant, in inches:",
                 anchor='e',
                 justify=tk.RIGHT,
                 bg='white').grid(row=9,
                                  column=5,
                                  columnspan=2)

        self.depth_per_plant_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT,
                                              relief='solid')
        self.depth_per_plant_entry.grid(row=9,
                                        column=7)
        tk.Label(self,
                 text="Depth to Plant Seeds, inches, 2 decimals ok:",
                 anchor='e',
                 justify=tk.RIGHT,
                 bg='white').grid(row=10,
                                  column=5,
                                  columnspan=2)

        self.depth_for_seeds_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT,
                                              bg='white',
                                              relief='solid')
        self.depth_for_seeds_entry.grid(row=10,
                                        column=7)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=11,
                                  column=1)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=12,
                                  column=1,
                                  columnspan=2)
        tk.Label(self,
                 text="Days to Harvest:",
                 anchor='e',
                 justify=tk.RIGHT,
                 bg='white').grid(row=12,
                                  column=3)

        self.days_to_harvest_entry = tk.Entry(self,
                                              width=5,
                                              justify=tk.LEFT,
                                              bg='white',
                                              relief='solid')
        self.days_to_harvest_entry.grid(row=12,
                                        column=4)

        tk.Label(self,
                 text="Watering Frequency:",
                 bg='white').grid(row=12,
                                  column=5,
                                  columnspan=1)

        self.watering_requirement_combo = DropDown(self,
                                                   watering_requirement_query,
                                                   12,
                                                   6,
                                                   1,
                                                   'W')
        self.new_plant = plant.Plant()

        tk.Button(self,
                  text="Add Plant",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  width=15,
                  command=lambda: self.add_new_plant(controller)).grid(row=12,
                                                                       column=8)

    def add_new_plant(self, controller):
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
        self.plant_in_spring = None
        self.plant_in_fall = None
        self.days_to_harvest = None
        self.plant_active = None
        self.times_succeeded = None
        self.total_times_planted = None

        try:

            # set variables to values input onscreen

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

            # create a new plant object to insert into database
            new_plant = plant.Plant()

            # pass new plant object to Plant class function to add plant
            # which returns a message if successful, otherwise would be NoneType.

            message = new_plant.add_plant(self.plant_name,
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

            # display success message in a popup window
            if message:
                controller.open_popup(controller,
                                      message)

            # exception handling if entry into database fails
            else:
                error_message = "Error inserting into database, new plant not added."
                controller.open_popup(controller,
                                      error_message)

        # exception handling for invalid data entry
        except TypeError:
            error_message = "Missing or invalid data, new plant not added."
            controller.open_popup(controller,
                                  error_message)


# class to create new planting instances, or plant sets
# and add them to a new plan automatically or manually
class GardenPlanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,
                          parent)
        tk.Label(self,
                 text="Create Garden Plan",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)

        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')
        tk.Label(self,
                 text="Please complete the following for all Garden Plans:",
                 font=MEDIUM_FONT,
                 bg='white',
                 fg='dark green',
                 anchor='w',
                 justify=tk.LEFT).grid(row=3,
                                       column=2,
                                       columnspan=5)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)
        tk.Label(self,
                 text="Select Plant Name:",
                 bg='white').grid(row=5,
                                  column=1,
                                  columnspan=2)

        self.plant_combo = DropDown(self,
                                    plant_name_query,
                                    5,
                                    3,
                                    2,
                                    'W')
        tk.Label(self,
                 text="Click Refresh if new plants have been added",
                 bg='white',
                 justify=tk.RIGHT,
                 anchor='e').grid(row=5,
                                  column=4,
                                  columnspan=3)
        tk.Button(self,
                  text="Refresh",
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  width=5,
                  command=self.reset_plant_dropdown).grid(row=5,
                                                          column=7,
                                                          sticky='EW')
        tk.Label(self,
                 text="Set Type:",
                 bg='white').grid(row=6,
                                  column=1,
                                  columnspan=2)

        self.set_type_combo = DropDown(self,
                                       set_type_query,
                                       6,
                                       3,
                                       1,
                                       'W')
        tk.Label(self,
                 text="Quantity:",
                 bg='white').grid(row=7,
                                  column=1,
                                  columnspan=2)

        self.quantity_entry = tk.Entry(self,
                                       width=22,
                                       justify=tk.LEFT,
                                       relief=tk.SOLID)
        self.quantity_entry.grid(row=7,
                                 column=3)
        tk.Button(self,
                  text="Add Plant to Auto-Plan",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.add(controller)).grid(row=7,
                                                             column=8,
                                                             sticky='EW')
        tk.Button(self,
                  text="Complete Auto-Plan",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.complete(controller)).grid(row=9,
                                                                  column=8,
                                                                  sticky='EW')
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=8,
                                  column=1)
        tk.Label(self,
                 text="For Manual Plans Only",
                 font=MEDIUM_FONT,
                 bg='white',
                 fg='dark green',
                 anchor='w',
                 justify=tk.LEFT).grid(row=10,
                                       column=2,
                                       columnspan=3)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=11,
                                  column=1)

        tk.Label(self,
                 text="Select your Season:",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=12,
                                  column=1,
                                  columnspan=2)

        self.season_combo = DropDown(self,
                                     seasons_query,
                                     12,
                                     3,
                                     1,
                                     'W')
        tk.Label(self,
                 text="Enter a Plot ID if known, or enter a Zone, Row and Column",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=13,
                                  column=2,
                                  columnspan=3)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=13,
                                  column=1)

        # setup spinbox with highest plot ID number as max value
        self.plot_stat_list = []
        top_plot_id = 1
        top_zone_id = 1
        top_row = 1
        top_column = 1

        try:

            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(plot_data_query)  # CAN REMOVE SOME OF THESE ASSIGNMENTS IF NOT  USED
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

                # don't include inactive plots
                if r[11] == 0:
                    continue

                # error handling if no plots have been set up yet
                # message displays as soon as program launches

                elif r[0] is None:
                    error_message = ("To start your first Garden Plan\n "
                                     "Add at least one new Zone and Plot\n"
                                     "under Garden Setup")
                    controller.open_popup(controller, error_message)

                    # set plot and zone spinbox values
                else:
                    if r[0] > top_plot_id:
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

            tk.Label(self,
                     text="Plot ID Number:",
                     justify=tk.RIGHT,
                     anchor='e',
                     bg='white').grid(row=14,
                                      column=1,
                                      columnspan=2)

            # spinbox for the plot, max value set above

            self.plot_spinbox = tk.Spinbox(self,
                                           from_=0,
                                           to=top_plot_id)
            self.plot_spinbox.grid(row=14,
                                   column=3)

            # Initiate the manual plan, which checks a selected plot
            # instead of assigning automatically

            tk.Button(self,
                      text="Check Plot / Instant Add",
                      bg='dark green',
                      fg='white',
                      font='Helvetica 10',
                      command=lambda: self.add_manual_set(controller)).grid(row=13,
                                                                            column=8,
                                                                            sticky='EW')

            tk.Label(self,
                     text="Zone Name:",
                     justify=tk.RIGHT,
                     anchor='e',
                     bg='white').grid(row=14,
                                      column=5,
                                      columnspan=2)

            self.zone_combo = DropDown(self,
                                       zone_query,
                                       14,
                                       7,
                                       1,
                                       'W')

            tk.Label(self,
                     text="Row Number:",
                     justify=tk.RIGHT,
                     anchor='e',
                     bg='white').grid(row=15,
                                      column=5,
                                      columnspan=2)

            # spinbox for the row number, max value set above

            self.row_spinbox = tk.Spinbox(self,
                                          from_=0,
                                          to=top_row)
            self.row_spinbox.grid(row=15,
                                  column=7)

            tk.Label(self,
                     text="Column Number:",
                     justify=tk.RIGHT,
                     anchor='e',
                     bg='white').grid(row=16,
                                      column=5,
                                      columnspan=2)

            # spinbox for the column number, max value set above

            self.col_spinbox = tk.Spinbox(self,
                                          from_=0,
                                          to=top_column)
            self.col_spinbox.grid(row=16,
                                  column=7)

            self.new_plan = plan.Plan()

        except:
            print("no connection available for spinbox")

    def add(self, controller):
        self.set_quantity = None
        self.plant_id = None
        self.my_season_id = None
        self.plot_id = None
        self.set_type_id = None

        try:

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

            success_message = (str(self.set_quantity) + " " + set_type  # CHANGE TO POPUP
                               + " of " + plant + " added to tentative Garden Plan")

            controller.open_popup(controller,
                                  success_message)


        # exception handling for invalid data entry
        except TypeError:
            error_message = "Missing or invalid data, plant set not added."
            controller.open_popup(controller,
                                  error_message)

    def complete(self, controller):
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

            if plot_id is None:

                error_message = ("No plots found.\n"
                                 "Please add least one Plot\n"
                                 "under Garden Setup")
                controller.open_popup(controller, error_message)

                return

            else:

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

        if self.new_plan.plant_set_list:

            message = self.new_plan.execute_plan()
            controller.open_popup(controller, message)


        else:
            error_message = ("No plant selected.\n"
                             "Please select at least one plant to add.")
            controller.open_popup(controller, error_message)

    def add_manual_set(self, controller):

        self.set_quantity = None
        self.plant_id = None
        self.my_season_id = None
        self.set_plot_id = None
        self.set_type_id = None
        self.zone_id = None
        self.row = None
        self.column = None

        try:

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

            this_manual_plan = plan.Plan()
            message = this_manual_plan.manual_plan(self.new_plant_set,
                                                   self.my_season_id,
                                                   self.set_plot_id,
                                                   self.zone_id,
                                                   self.row,
                                                   self.column)

            controller.open_popup(controller, message)


        except TypeError:
            error_message = "Missing or invalid data, plant set not added."
            controller.open_popup(controller,
                                  error_message)

    def reset_plant_dropdown(self):
        self.plant_combo = DropDown(self,
                                    plant_name_query,
                                    3,
                                    2,
                                    2,
                                    'W')
class EditSetPage(tk.Frame):

    def __init__(self,
                 parent,
                 controller):
        tk.Frame.__init__(self,
                          parent)

        self.set_default_values(controller)

    # set values that display when the window first loads

    def set_default_values(self, controller):

        tk.Label(self,
                 text="Edit Plant Set",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=7,
                                                                         sticky='EW')

        tk.Label(self,
                 text="Select Plant Name:",
                 bg='white',
                 font='bold').grid(row=3,
                                  column=1,
                                  columnspan=1)

        self.plant_combo = DropDown(self,
                                    planting_plan_query,
                                    3,
                                    2,
                                    1,
                                    'W')

        tk.Label(self,
                 text="Season:",
                 font='bold',
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=3,
                                  column=3,
                                  columnspan=1)

        self.season_combo = DropDown(self,
                                     seasons_query,
                                     3,
                                     4,
                                     1,
                                     'W')

        tk.Button(self,
                  width=10,
                  text="Search",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.import_plant_set(controller)).grid(row=3,
                                 column=5,
                                 sticky='E')

        tk.Button(self,
                  text="Next in Season",
                  width=15,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.import_next_plant_set(controller)).grid(row=3,
                                 column=6,
                                 sticky='E')

        self.search_error = tk.Label(self)  # DELETE THIS ONCE CONFIRMED REMOVED USAGE ELSEWHERE

        tk.Label(self,
                 text=" ",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=4,
                                  column=1,
                                  columnspan=1)

        tk.Label(self,
                 text="Plant Set ID:",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=5,
                                  column=1,
                                  columnspan=1)

        self.plant_set_id = tk.IntVar()
        self.plant_set_id.set(0)

        tk.Label(self,
                 textvariable=self.plant_set_id,
                 bg='white').grid(row=5,
                                  column=2)

        tk.Label(self,
                 text="Set Type:",
                 bg='white').grid(row=5,
                                  column=4)

        self.set_type_combo = DropDown(self,
                                       set_type_query,
                                       5,
                                       5,
                                       1,
                                       'W')

        tk.Label(self,
                 text="Quantity:",
                 bg='white').grid(row=6,
                                  column=4)

        self.quantity_entry = tk.Entry(self,
                                       width=5,
                                       justify=tk.LEFT,
                                       bg='white',
                                       relief='solid')
        self.quantity_entry.grid(row=6,
                                 column=5)

        tk.Label(self,
                 text="Plot ID Number:",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=6,
                                  column=1,
                                  columnspan=1)

        self.plot_id = '0'
        self.plot_entry = tk.Entry(self,
                                   width=5,
                                   bg='white',
                                   relief='solid')
        self.plot_entry.grid(row=6,
                             column=2)
        self.plot_entry.insert(0, self.plot_id)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=8,
                                  column=1)

        tk.Label(self,
                 text="Plant Set Notes (Optional):",
                 bg='white').grid(row=8,
                                  column=1,
                                  columnspan=1)

        self.set_notes_text = tk.Text(self,
                                      height=3,
                                      width=30,
                                      bg='white',
                                      relief='solid')
        self.set_notes_text.grid(row=8,
                                 column=2,
                                 columnspan=2)

        tk.Label(self,
                 text="Date Planted:",
                 bg='white').grid(row=7,
                                  column=5,
                                  columnspan=2)

        self.date_planted_entry = tk.Entry(self,
                                           width=10,
                                           bg='white',
                                           relief='solid')
        self.date_planted_entry.grid(row=7,
                                     column=7)

        tk.Label(self,
                 text="First Harvest Date (MM/DD/YY):",
                 bg='white').grid(row=8,
                                  column=5,
                                  columnspan=2)

        self.first_harvest_entry = tk.Entry(self,
                                            width=10,
                                            bg='white',
                                            relief='solid')
        self.first_harvest_entry.grid(row=8,
                                      column=7)

        tk.Label(self,
                 text="Last Harvest Date (MM/DD/YY)",
                 bg='white',).grid(row=9,
                                  column=5,
                                  columnspan=2)

        self.last_harvest_entry = tk.Entry(self,
                                           width=10,
                                           bg='white',
                                           relief='solid')
        self.last_harvest_entry.grid(row=9,
                                     column=7)

        # Function to retrieve selection from the Outcome Radio button

        def select_radio():
            self.radio_selection = outcome_radio_entry.get()
            print(self.radio_selection)

        # Outcome radio button label and option setup

        tk.Label(self,
                 text="Outcome:",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=10,
                                  column=1)

        outcome_radio_entry = tk.IntVar()  # stores selection value
        self.radio_selection = None

        self.radio1 = tk.Radiobutton(self,
                                     text="Pending",
                                     bg='white',
                                     variable=outcome_radio_entry,
                                     value=9,
                                     command=select_radio)
        self.radio1.grid(row=10,
                         column=2)

        self.radio2 = tk.Radiobutton(self,
                                     text="Success",
                                     bg='white',
                                     variable=outcome_radio_entry,
                                     value=1,
                                     command=select_radio)
        self.radio2.grid(row=10,
                         column=3)

        self.radio3 = tk.Radiobutton(self,
                                     text="Failure",
                                     bg='white',
                                     variable=outcome_radio_entry,
                                     value=0,
                                     command=select_radio)
        self.radio3.grid(row=10,
                         column=4)

        self.radio1.select()  # default selection of Pending

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=11,
                                  column=1)

        tk.Button(self,
                  text="Check and Save Changes",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.check_edited_set(controller)).grid(row=13,
                                                                          column=7,
                                                                          sticky='EW')

        tk.Button(self,
                  text="Save Without Checking",
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.save_unchecked_set(controller)).grid(row=13,
                                                                            column=5,
                                                                            sticky='EW')

        # variables to store search criteria that comes from dropdowns
        # plant_set_id is set further up

        self.plant_name = None
        self.season_text = None

    def import_plant_set(self, controller):

        self.saved_plant_set = plant_set.PlantSet()
        plant_selection = self.plant_combo.selection
        season_selection = self.season_combo.selection
        set_to_check = 0

        q_plant_set_id = self.saved_plant_set.import_plant_set(plant_selection,
                                                               season_selection,
                                                               set_to_check)

        if q_plant_set_id is None and set_to_check == 0:

            error_text = "Plant Not Found"
            controller.open_popup(controller, error_text)

            self.set_default_values(controller)

        elif q_plant_set_id is None and set_to_check > 0:

            error_text = "Last in Season"
            controller.open_popup(controller, error_text)

        else:
            self.plant_set_id.set(q_plant_set_id)
            self.saved_plant_set.plant_set_id = self.plant_set_id.get()

            self.saved_plot_id = self.saved_plant_set.plot_id

            self.reset_values(controller)

    def import_next_plant_set(self, controller):

        self.saved_plant_set = plant_set.PlantSet()
        plant_selection = self.plant_combo.selection
        season_selection = self.season_combo.selection
        set_to_check = self.plant_set_id.get()

        q_plant_set_id = self.saved_plant_set.import_plant_set(plant_selection,
                                                               season_selection,
                                                               set_to_check)

        if q_plant_set_id is None and set_to_check == 0:

            error_text = "Plant Not Found"
            controller.open_popup(controller, error_text)

            self.set_default_values(controller)

        elif q_plant_set_id is None and set_to_check > 0:

            error_text = "Last in Season"
            controller.open_popup(controller, error_text)

        else:
            self.plant_set_id.set(q_plant_set_id)
            self.saved_plant_set.plant_set_id = self.plant_set_id.get()

            self.saved_plot_id = self.saved_plant_set.plot_id

            self.reset_values(controller)

    def reset_values(self, controller):

        try:

            self.plant_set_id.set(self.saved_plant_set.plant_set_id)

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

        except TypeError:
            error_text = "Error resetting values"
            controller.open_popup(controller, error_text)

    def check_edited_set(self, controller):

        try:

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
            self.updated_set.add_new_plant_set(self.plant_id, self.set_type_id, self.set_quantity)

            # check if plot was changed
            self.plot_change = None
            if int(self.plot_id) == int(self.saved_plot_id):
                self.plot_change = 'N'
            else:
                self.plot_change = 'Y'

            self.edited_plan = plan.Plan()
            self.confirmed_plan = self.edited_plan.edited_plan_checks(self.updated_set,
                                                                      self.season_id,
                                                                      self.plot_id,
                                                                      self.plot_change)

            if self.confirmed_plan:
                self.export_edited_set(controller)

            else:
                error_message = "Failed checks, plant set not updated."
                controller.open_popup(controller,
                                      error_message)

        except:
            error_message = "Missing or invalid data, plant set not updated."
            controller.open_popup(controller,
                                  error_message)

    def save_unchecked_set(self, controller):

        try:

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
            self.updated_set.add_new_plant_set(self.plant_id, self.set_type_id, self.set_quantity)

            self.export_edited_set(controller)

        except:
            error_message = "Missing or invalid data, plant set not added."
            controller.open_popup(controller,
                                  error_message)

    def export_edited_set(self, controller):

        try:

            self.updated_set.export_updated_set(
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

            success_message = "Plant set updated successfully"
            controller.open_popup(controller,
                                  success_message)

        except:
            error_message = "Error exporting, plant set not updated."
            controller.open_popup(controller,
                                  error_message)


# class to display the Setup Menu page
class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self,
                 text="Setup Menu",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)

        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')
        tk.Label(self,
                 text=" ",
                 width='5',
                 bg='white').grid(row=3,
                                  column=1)
        tk.Label(self,
                 text=" ",
                 width='5',
                 bg='white').grid(row=4,
                                  column=1)
        tk.Button(self,
                  width=20,
                  text="Add New Zone",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(AddZonesPage)).grid(row=4,
                                                                            column=2,
                                                                            sticky='W')
        tk.Label(self,
                 text=" ",
                 width='5',
                 bg='white').grid(row=4,
                                  column=3)
        tk.Button(self,
                  width=20,
                  text="Add New Plots",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(AddPlotsPage)).grid(row=4,
                                                                            column=4,
                                                                            sticky='W')
        tk.Label(self,
                 text=" ",
                 width='5',
                 bg='white').grid(row=4,
                                  column=5)
        tk.Button(self,
                  width=20,
                  text="Add New Season",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(AddSeasonPage)).grid(row=4,
                                                                             column=6,
                                                                             sticky='W')
        tk.Label(self,
                 text=" ",
                 width='5',
                 bg='white').grid(row=5,
                                  column=3)
        tk.Label(self,
                 text="Brand new? Start by adding New Zones, Plots, then Seasons above.",
                 justify=tk.LEFT,
                 anchor='w',
                 bg='white',
                 fg='dark green',
                 font=MEDIUM_FONT).grid(row=6,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 width='5',
                 bg='white').grid(row=7,
                                  column=3)

        tk.Button(self,
                  width=20,
                  text="Edit Existing Plot",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(EditPlotPage)).grid(row=8,
                                                                            column=4,
                                                                            sticky='W')

        tk.Button(self,
                  width=20,
                  text="Edit Plant Set",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(EditSetPage)).grid(row=8,
                                                                           column=2,
                                                                           sticky='E')


# class to add new Zones to the database
# a Zone is a contiguous set of plots
class AddZonesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self,
                 text="New / Edit Zone",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)

        tk.Button(self,
                  text="Back to Setup Menu",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(SetupPage)).grid(row=2,
                                                                         column=6,
                                                                         sticky='EW')
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=3,
                                  column=1)

        tk.Label(self,
                 text='A "plot" is a space where a single plant'
                      ' or plant set can be planted.',
                 bg='white').grid(row=4,
                                  column=1,
                                  columnspan=8)
        tk.Label(self,
                 text='A "Zone" is a group of contiguous plots,'
                      ' such as a designated garden area or raised bed',
                 bg='white').grid(row=5,
                                  column=1,
                                  columnspan=8)
        tk.Label(self,
                 text="",
                 bg='white').grid(row=6,
                                  column=2)
        tk.Label(self,
                 text='Please enter a unique name for your zone: ',
                 bg='white').grid(row=7,
                                  column=1,
                                  columnspan=4)
        tk.Label(self,
                 text='Ex. "Large Garden, Blue Flowerpot 1',
                 bg='white').grid(row=8,
                                  column=1,
                                  columnspan=5)
        self.zone_name_entry = tk.Entry(self,
                                        justify=tk.LEFT,
                                        width=40,
                                        bg='white')
        self.zone_name_entry.grid(row=7,
                                  column=5,
                                  columnspan=3)
        tk.Label(self,
                 text="",
                 bg='white').grid(row=9,
                                  column=2)

        tk.Label(self,
                 text="Number of rows of plots in this zone:",
                 bg='white').grid(row=10,
                                  column=1,
                                  columnspan=4)
        self.zone_rows_entry = tk.Entry(self,
                                        justify=tk.LEFT,
                                        width=5,
                                        bg='white')
        self.zone_rows_entry.grid(row=10,
                                  column=5)
        tk.Label(self,
                 text="Number of columns of plots in this zone:",
                 bg='white').grid(row=11,
                                  column=1,
                                  columnspan=4)
        self.zone_columns_entry = tk.Entry(self,
                                           justify=tk.LEFT,
                                           width=5,
                                           bg='white')
        self.zone_columns_entry.grid(row=11,
                                     column=5)

        tk.Label(self,
                 text="",
                 bg='white').grid(row=12,
                                  column=2)

        tk.Label(self,
                 text="Zone Notes (Optional):",
                 bg='white').grid(row=13,
                                  column=1,
                                  columnspan=2)
        self.zone_notes_text = tk.Text(self,
                                       height=3,
                                       width=20,
                                       bg='white')
        self.zone_notes_text.grid(row=13,
                                  column=3,
                                  columnspan=3)
        tk.Button(self,
                  text="Add Zone",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.add_new_zone(controller)).grid(row=13,
                                                                      column=8,
                                                                      sticky='EW')

    def add_new_zone(self, controller):
        self.zone_rows = None
        self.zone_columns = None
        self.zone_notes = None  # in case left blank

        try:

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

            this_connection.end_connection()

            #display confirmation popup
            success_message = ('Finished Inserting the following Zone: '
                               + self.zone_name)
            controller.open_popup(controller,
                                  success_message)

        # error handling for missing or invalid data
        except:
            error_message = "Missing or invalid data, zone not added."
            controller.open_popup(controller,
                                  error_message)


class AddPlotsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self,
                 text="Add New Plots",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  text="Back to Setup Menu",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(SetupPage)).grid(row=2,
                                                                         column=6,
                                                                         sticky='EW')
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Label(self,
                 text="Please select a Zone:",
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        self.zone_combo = DropDown(self,
                                   zone_query,
                                   3,
                                   3,
                                   2,
                                   'W')

        tk.Label(self,
                 text="Click Refresh if new zones have been added:",
                 bg='white').grid(row=3,
                                  column=5,
                                  columnspan=3)

        tk.Button(self,
                  text="Refresh",
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=self.reset_zone_dropdown).grid(row=3,
                                                         column=8,
                                                         sticky='E')

        tk.Label(self,
                 text="Number of rows of identical plots to add:",
                 bg='white').grid(row=4,
                                  column=1,
                                  columnspan=3)

        self.quantity_rows_entry = tk.Entry(self,
                                            width=5,
                                            relief=tk.SOLID)
        self.quantity_rows_entry.grid(row=4,
                                      column=4)

        tk.Label(self,
                 text="Number of columns of identical plots to add:",
                 bg='white').grid(row=5,
                                  column=1,
                                  columnspan=3)

        self.quantity_columns_entry = tk.Entry(self,
                                               width=5,
                                               bg='white',
                                               relief=tk.SOLID)
        self.quantity_columns_entry.grid(row=5,
                                         column=4)

        tk.Label(self,
                 text="Size of each Plot:",
                 anchor='e',
                 justify=tk.RIGHT,
                 bg='white').grid(row=6,
                                  column=1)

        self.plot_size_entry = tk.Entry(self,
                                        width=5,
                                        justify=tk.LEFT,
                                        bg='white',
                                        relief=tk.SOLID)
        self.plot_size_entry.grid(row=6,
                                  column=2)

        tk.Label(self,
                 text="Unit of Measurement:",
                 bg='white').grid(row=6,
                                  column=3,
                                  columnspan=2)

        self.measurement_combo = DropDown(self,
                                          measurement_unit_query,
                                          6,
                                          5,
                                          2,
                                          'W')

        tk.Label(self,
                 text="",
                 bg='white').grid(row=7,
                                  column=1)

        self.is_container = tk.IntVar()
        self.is_container_checkbox \
            = (tk.Checkbutton(self,
                              text="Is this plot a container (solid bottom)?",
                              bg='white',
                              variable=self.is_container,
                              onvalue=1,
                              offvalue=0,
                              width=40,
                              justify=tk.LEFT,
                              anchor='w'))
        self.is_container_checkbox.grid(row=7,
                                        column=2,
                                        columnspan=3)

        tk.Label(self,
                 text="If container, container depth in inches:",
                 bg='white').grid(row=8,
                                  column=3,
                                  columnspan=3)

        self.container_depth_entry = tk.Entry(self,
                                              width=5,
                                              relief=tk.SOLID)
        self.container_depth_entry.grid(row=8,
                                        column=6)

        tk.Label(self,
                 text="Sun Level of Plot(s):",
                 bg='white').grid(row=9,
                                  column=1,
                                  columnspan=2)

        self.sun_combo = DropDown(self,
                                  sun_query,
                                  9,
                                  3,
                                  2,
                                  'W')

        tk.Label(self,
                 text="Soil Moisture Level of Plot(s):",
                 bg='white').grid(row=9,
                                  column=5,
                                  columnspan=2)

        self.soil_moisture_combo = DropDown(self,
                                            soil_moisture_query,
                                            9,
                                            7,
                                            2,
                                            'W')

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=10,
                                  column=5,
                                  columnspan=2)

        tk.Button(self, text="Add Plots",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.add_new_plots(controller)).grid(row=11,
                                                                       column=8,
                                                                       sticky='EW')

    def add_new_plots(self, controller):
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

        try:

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

            #display confirmation popup
            success_message = ('Plots added successfully!')
            controller.open_popup(controller,
                                  success_message)

        # error handling for missing or invalid data
        except:
            error_message = "Missing or invalid data, plots not added."
            controller.open_popup(controller,
                                  error_message)

    def reset_zone_dropdown(self):
        self.zone_combo = DropDown(self,
                                   zone_query,
                                   3,
                                   3,
                                   2,
                                   'W')


class EditPlotPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        try:

            self.set_default_values(controller)
            self.set_plot_spinbox(controller)

        except:
            print("no connection available")

    def set_default_values(self, controller):
        tk.Label(self,
                 text="Edit Individual Plot",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  text="Back to Setup Menu",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(SetupPage)).grid(row=2,
                                                                         column=6,
                                                                         sticky='EW')
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Button(self,
                  width=10,
                  text="Search",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.import_plot(controller)).grid(row=3,
                                 column=4,
                                 sticky='E')

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=10,
                                  column=1,
                                  columnspan=5)

        tk.Button(self, text="Save Changes",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_edited_plot(controller)).grid(row=11,
                                                                            column=8,
                                                                            sticky='EW')
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1,
                                  columnspan=5)

        tk.Label(self,
                 text="Size of Plot:",
                 anchor='e',
                 justify=tk.RIGHT,
                 bg='white').grid(row=5,
                                  column=2)

        self.plot_size_entry = tk.Entry(self,
                                        width=5,
                                        justify=tk.LEFT,
                                        bg='white',
                                        relief=tk.SOLID)
        self.plot_size_entry.grid(row=5,
                                  column=3)
        tk.Label(self,
                 text="Unit of Measurement:",
                 bg='white').grid(row=5,
                                  column=4,
                                  columnspan=2)

        self.measurement_combo = DropDown(self,
                                          measurement_unit_query,
                                          5,
                                          6,
                                          1,
                                          'W')
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=6,
                                  column=1,
                                  columnspan=5)
        tk.Label(self,
                 text="Sun Level of Plot:",
                 bg='white').grid(row=7,
                                  column=1,
                                  columnspan=2)

        self.sun_combo = DropDown(self,
                                  sun_query,
                                  7,
                                  3,
                                  2,
                                  'W')

        tk.Label(self,
                 text="Soil Moisture Level of Plot:",
                 bg='white').grid(row=8,
                                  column=1,
                                  columnspan=2)

        self.soil_moisture_combo = DropDown(self,
                                            soil_moisture_query,
                                            8,
                                            3,
                                            1,
                                            'W')

        tk.Label(self,
                 text="Current Nitrogen Level of Plot:",
                 bg='white').grid(row=8,
                                  column=4,
                                  columnspan=2)

        self.nitrogen_level = tk.IntVar()
        self.nitrogen_level_entry = tk.Entry(self,
                                             width=5,
                                             bg='white',
                                             relief=tk.SOLID)
        self.nitrogen_level_entry.grid(row=8,
                                       column=6)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=9,
                                  column=1,
                                  columnspan=5)

        self.is_container = tk.IntVar()
        self.is_container_checkbox \
            = (tk.Checkbutton(self,
                              text="Is this plot a container (solid bottom)?",
                              bg='white',
                              variable=self.is_container,
                              onvalue=1,
                              offvalue=0,
                              width=40,
                              justify=tk.LEFT,
                              anchor='w'))
        self.is_container_checkbox.grid(row=10,
                                        column=2,
                                        columnspan=3)

        tk.Label(self,
                 text="If container, container depth in inches:",
                 bg='white').grid(row=11,
                                  column=3,
                                  columnspan=2)

        self.container_depth_entry = tk.Entry(self,
                                              width=5,
                                              bg='white',
                                              relief=tk.SOLID)
        self.container_depth_entry.grid(row=11,
                                        column=5)

        self.plot_active = tk.IntVar()
        self.plot_active_checkbox \
            = (tk.Checkbutton(self,
                              text="Plot Active",
                              bg='white',
                              variable=self.plot_active,
                              onvalue=1,
                              offvalue=0,
                              width=20,
                              justify=tk.RIGHT,
                              anchor='e'))
        self.plot_active_checkbox.grid(row=12,
                                       column=2)

    def set_plot_spinbox(self, controller):
        # setup spinbox with highest plot ID number as max value
        self.plot_stat_list = []
        top_plot_id = 1

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
            self.this_plot.set_plot_values(  # NEED ALL DUE TO FUNCTION PARAMETERS
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

            # if no plots have been added, top plot ID set to 0
            # error handling will occur when search button clicked
            if r[0] is None:
                top_plot_id = 0

            # set plot spinbox max value
            else:
                if r[0] > top_plot_id:
                    top_plot_id = r[0]

        tk.Label(self,
                 text="Enter Plot ID to Edit:",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white',
                 font='bold').grid(row=3,
                                  column=1,
                                  columnspan=2)

        # spinbox for the plot, max value set above

        self.plot_spinbox = tk.Spinbox(self,
                                       from_=0,
                                       to=top_plot_id,
                                       width=5)
        self.plot_spinbox.grid(row=3,
                               column=3)

    def import_plot(self, controller):
        self.saved_plot = plot.Plot()
        plot_id = self.plot_spinbox.get()

        print(plot_id)
        self.plot_id = self.saved_plot.import_plot(plot_id)

        if self.plot_id is None:

            error_text = "Plot Not Found"
            controller.open_popup(controller, error_text)
        else:

            print(self.plot_id)

        if self.plot_id is not None:
            self.reset_values(controller)
        else:
            self.set_default_values(controller)

    def reset_values(self, controller):
        self.container_depth_entry.delete(0, 'end')
        self.plot_active = 0
        self.plot_active_checkbox.deselect()
        self.is_container = 0
        self.is_container_checkbox.deselect()

        if self.saved_plot.plot_active is True:
            self.plot_active = 1
            self.plot_active_checkbox.select()

        else:
            self.plot_active = 0

        self.plot_size_entry.delete(0, 'end')
        self.plot_size_entry.insert(0, self.saved_plot.plot_size)

        self.nitrogen_level_entry.delete(0, 'end')
        self.nitrogen_level_entry.insert(0, self.saved_plot.plot_nitrogen_level)

        measurement_unit = self.get_id_value(measurement_unit_query, self.saved_plot.measurement_unit_id)
        self.measurement_combo.combo.set(measurement_unit)

        sun = self.get_id_value(sun_query, self.saved_plot.sun_id)
        self.sun_combo.combo.set(sun)

        soil_moisture = self.get_id_value(soil_moisture_query, self.saved_plot.soil_moisture_id)
        self.soil_moisture_combo.combo.set(soil_moisture)

        if self.saved_plot.is_container is True:
            self.is_container = 1
            self.is_container_checkbox.select()
            self.container_depth_entry.insert(0, self.saved_plot.container_depth)

        else:
            self.is_container = 0

    def export_edited_plot(self, controller):

        try:

            self.plot_size = self.plot_size_entry.get()

            measurement_unit = self.measurement_combo.combo.get()
            self.measurement_unit_id = self.measurement_combo.get_id(measurement_unit_query, measurement_unit)

            if self.is_container == 1:
                self.container = bool(True)
                self.container_depth = int(self.container_depth_entry.get())
            else:
                self.container = bool(False)
                self.container_depth = None

            self.nitrogen_level = self.nitrogen_level_entry.get()

            sun = self.sun_combo.combo.get()
            self.sun_id = self.sun_combo.get_id(sun_query, sun)

            soil_moisture = self.soil_moisture_combo.combo.get()
            self.soil_moisture_id = self.soil_moisture_combo.get_id(soil_moisture_query, soil_moisture)

            if self.plot_active == 1:
                self.is_active = bool(True)
            else:
                self.is_active = bool(False)

            self.edited_plot = plot.Plot()
            self.edited_plot.export_updated_plot(self.plot_id,
                                                 self.plot_size,
                                                 self.measurement_unit_id,
                                                 self.container,
                                                 self.container_depth,
                                                 self.nitrogen_level,
                                                 self.sun_id,
                                                 self.soil_moisture_id,
                                                 self.is_active)


        except:
            error_message = "Missing or invalid data, season not updated."
            controller.open_popup(controller,
                                  error_message)

    def get_id_value(self,
                     query_name,
                     id):
        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor
        cursor.execute(query_name)
        records = cursor.fetchall()
        for r in records:
            if id == r[0]:
                self.value = r[1]
                this_connection.end_connection()
                return self.value


class AddSeasonPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self,
                 text="Add New Season",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  text="Back to Setup Menu",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(SetupPage)).grid(row=2,
                                                                         column=6,
                                                                         sticky='EW')
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Label(self,
                 text="Select Season:",
                 font='bold',
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        self.season_radio_entry = tk.IntVar()
        self.radio_selection = 0

        self.radio1 = tk.Radiobutton(self,
                                     text="Spring",
                                     bg='white',
                                     justify=tk.RIGHT,
                                     anchor='e',
                                     variable=self.season_radio_entry,
                                     value=1,
                                     command=self.select_radio)
        self.radio1.grid(row=3,
                         column=3)

        self.radio2 = tk.Radiobutton(self,
                                     text="Fall",
                                     bg='white',
                                     justify=tk.RIGHT,
                                     anchor='e',
                                     variable=self.season_radio_entry,
                                     value=2,
                                     command=self.select_radio)
        self.radio2.grid(row=3,
                         column=4)

        tk.Label(self,
                 text="",
                 bg='white').grid(row=4,
                                  column=2)

        tk.Label(self,
                 text="Enter Year:",
                 font='bold',
                 bg='white').grid(row=5,
                                  column=1,
                                  columnspan=2)

        self.year_spinbox = tk.Spinbox(self,
                                       from_=2020,
                                       to=3000,
                                       width=10)
        self.year_spinbox.grid(row=5,
                               column=3)

        tk.Button(self,
                           text="Generate My Season",
                           bg='dark green',
                           fg='white',
                           font='Helvetica 10',
                           command=lambda: self.add_new_season(controller)).grid(row=5,
                    column=5,
                    sticky='EW')

    def select_radio(self):
        self.radio_selection = self.season_radio_entry.get()
        print(self.radio_selection)

    def add_new_season(self, controller):
        try:
            self.year = self.year_spinbox.get()

            if self.radio_selection == 1:
                self.season = "Spring"
            if self.radio_selection == 2:
                self.season = "Fall"

            new_season = my_season.MySeason()
            new_season.set_season_values(self.season, self.year)
            new_season_text = new_season.export_season()

            # display confirmation popup
            success_message = ("Season generated successfully:\n"
                               + new_season_text)
            controller.open_popup(controller,
                                  success_message)

            # error handling for missing or invalid data
        except:
            error_message = "Missing or invalid data, season not added."
            controller.open_popup(controller,
                                  error_message)


class EditSeasonPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.set_default_values()

        self.season_combo = DropDown(self,
                                     seasons_query,
                                     4,
                                     3,
                                     3,
                                     'E')
        tk.Button(self,
                  text="Back to Setup Menu",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(SetupPage)).grid(row=2,
                                                                         column=6,
                                                                         sticky='EW')
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')
        tk.Button(self,
                  width=5,
                  text="Go",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.import_my_season(controller)).grid(row=4,
                                                                          column=6,
                                                                          sticky='W')
        tk.Button(self,
                  text="Save Changes",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_edited_season(controller)).grid(row=8,
                                                                              column=8,
                                                                              sticky='EW')


    # set default label values, so they can persist when other data is reset
    def set_default_values(self):

        tk.Label(self,
                 text="Edit Season",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)

        tk.Label(self,
                 text="",
                 bg='white').grid(row=3,
                                  column=2)

        tk.Label(self,
                 text="Select Season:",
                 bg='white',
                 font=MEDIUM_FONT).grid(row=4,
                                  column=1,
                                  columnspan=2)
        tk.Label(self,
                 text="",
                 bg='white').grid(row=5,
                                  column=2)
        tk.Label(self,
                 text="Season Name:",
                 bg='white').grid(row=6,
                                  column=1,
                                  columnspan=2)

        self.season_radio_entry = tk.IntVar()
        self.radio_selection = 0

        self.radio1 = tk.Radiobutton(self,
                                     text="Spring",
                                     bg='white',
                                     justify=tk.RIGHT,
                                     anchor='e',
                                     variable=self.season_radio_entry,
                                     value=1,
                                     command=self.select_radio)
        self.radio1.grid(row=6,
                         column=3)

        self.radio2 = tk.Radiobutton(self,
                                     text="Fall",
                                     bg='white',
                                     justify=tk.RIGHT,
                                     anchor='e',
                                     variable=self.season_radio_entry,
                                     value=2,
                                     command=self.select_radio)
        self.radio2.grid(row=6,
                         column=4)
        tk.Label(self,
                 text="Year:",
                 bg='white',
                 justify=tk.LEFT).grid(row=7,
                                  column=1,
                                  columnspan=2)
        self.year = tk.IntVar()
        self.year.set(int(date.today().strftime("%Y")))
        self.year_spinbox = tk.Spinbox(self,
                                       from_=2020,
                                       to=3000,
                                       width=10,
                                       textvariable=self.year
                                       )
        self.year_spinbox.grid(row=7,
                               column=3)

        self.season_active = tk.IntVar()
        self.season_active_checkbox \
            = (tk.Checkbutton(self,
                              text="Season Active",
                              bg='white',
                              variable=self.season_active,
                              onvalue=1,
                              offvalue=0,
                              width=20,
                              justify=tk.LEFT,
                              anchor='w'))
        self.season_active_checkbox.grid(row=8,
                                         column=1,
                                         columnspan=3)

    def select_radio(self):
        self.radio_selection = self.season_radio_entry.get()

    def import_my_season(self, controller):
        self.saved_season = my_season.MySeason()
        season_selection = self.season_combo.selection
        season_id = self.season_combo.get_id(seasons_query,
                                             season_selection)

        self.season_id = self.saved_season.import_my_season(season_id)

        if self.season_id is None:

            error_text = "Season Not Found"
            controller.open_popup(controller, error_text)
        else:

            print(self.season_id)

        if self.season_id is not None:
            self.reset_values(controller)
        else:
            self.set_default_values()

    def reset_values(self, controller):

        if self.saved_season.spring == 1:
            self.radio1.select()
        elif self.saved_season.fall == 1:
            self.radio2.select()
        else:
            error_text = "Error importing season"
            controller.open_popup(controller, error_text)

        self.year.set(self.saved_season.my_season_year)

        self.season_active.set(self.saved_season.season_active)

    def export_edited_season(self, controller):

        try:

            self.my_season_text = self.season_combo.selection
            self.season_id = self.season_combo.get_id(seasons_query,
                                                      self.my_season_text)

            self.my_season_year = self.year_spinbox.get()

            true_season = self.season_radio_entry.get()

            print(true_season)

            if true_season == 1:
                self.spring = True
            else:
                self.spring = False

            if true_season == 2:
                self.fall = True
            else:
                self.fall = False

            self.is_active = self.season_active.get()

            self.updated_season = my_season.MySeason()

            self.updated_season.export_updated_season(self.season_id,
                                                      self.my_season_text,
                                                      self.my_season_year,
                                                      self.spring,
                                                      self.fall,
                                                      self.is_active)

            # display confirmation popup
            success_message = ('Season updated: '
                               + self.my_season_text)
            controller.open_popup(controller,
                                  success_message)

            # error handling for missing or invalid data
        except:
            error_message = "Missing or invalid data, season not updated."
            controller.open_popup(controller,
                                  error_message)


class DisplayPlan(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self,
                 text="Current Garden Plan",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Label(self,
                 text="Select your Season:",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white',
                 font='bold').grid(row=3,
                                  column=1,
                                  columnspan=2)

        self.season_combo = DropDown(self,
                                     seasons_query,
                                     3,
                                     3,
                                     1,
                                     'W')

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=3,
                                  column=5)

        tk.Button(self,
                  text="View Plan for Season",
                  bg='dark green',
                  fg='white',
                  command=lambda: self.view_season_plan(controller)).grid(row=3,
                                                                          column=6)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=3,
                                  column=7)

    def reset_grid(self):
        for label in self.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def view_season_plan(self, controller):

        self.reset_grid()

        tk.Label(self,
                 text="Current Garden Plan",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Label(self,
                 text="Select your Season:",
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white',
                 font=MEDIUM_FONT).grid(row=3,
                                  column=1,
                                  columnspan=2)

        self.set_season_id(controller)
        self.query_grid(display_grid_query, self.season_id, controller)

    def set_season_id(self, controller):
        season = self.season_combo.selection

        if season is None:
            error_message = "No season selected."
            controller.open_popup(controller,
                                  error_message)

        self.season_id = self.season_combo.get_id(seasons_query, season)

    def query_grid(self, display_grid_query, season_id, controller):

        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(display_grid_query + ' ?', [season_id])

            zone = ''
            max_row = 0
            last_row = 6
            max_column = 0

            tk.Label(self,
                     text=" ",
                     bg='white').grid(column=1,
                                      row=4)

            for row_number, data_row in enumerate(cursor):  # query is sorted by zones already
                current_zone = data_row[0]
                current_row = data_row[2]
                current_column = data_row[3] + 1
                current_plant = data_row[5]

                if zone == '':
                    tk.Label(self,
                             text=str(current_zone),
                             bg='white',
                             font=MEDIUM_FONT).grid(column=1,
                                              row=last_row)
                elif zone != current_zone:
                    last_row = last_row + max_row + 1
                    tk.Label(self,
                             text=' ',
                             bg='white').grid(column=1,
                                              row=last_row)
                    last_row = last_row + 1
                    tk.Label(self,
                             text=str(current_zone),
                             bg='white',
                             font=MEDIUM_FONT).grid(column=1,
                                              row=last_row)
                    max_row = 0
                else:
                    if current_row > max_row:
                        max_row = current_row

                tk.Label(self,
                         text=str(current_plant),
                         bg='white',
                         font='roman',
                         fg='dark green').grid(column=current_column,
                                          row=current_row + last_row)
                tk.Label(self,
                         text='Row ' + str(current_row),
                         bg='white').grid(column=1,
                                          row=current_row + last_row)

                if current_column >= max_column:
                    max_column = current_column

                zone = current_zone

            for column in range(1, max_column):
                tk.Label(self,
                         text='Column ' + str(column),
                         bg='white').grid(column=column + 1,
                                          row=5)

            this_connection.end_connection()

        except:
            error_message = "Error displaying Planting Plan"
            controller.open_popup(controller,
                                  error_message)


class ReportsMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        logo_file = "Logo.png"
        path = os.path.abspath(__file__)
        logo_dir = os.path.dirname(path)
        logo_path = os.path.join(logo_dir, logo_file)

        logo = tk.PhotoImage(file=logo_path)
        label = tk.Label(image=logo)
        label.image = logo

        tk.Label(self,
                 image=label.image, border=0).grid(row=3,
                                                   rowspan=6,
                                                   column=4,
                                                   columnspan=3)
        tk.Label(self,
                 text="Reports Menu",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')
        tk.Label(self,
                 text="Please Select a Report to View",
                 bg='white',
                 fg='dark green',
                 font=MEDIUM_FONT).grid(row=3,
                                        column=1,
                                        columnspan=3)
        tk.Button(self,
                  width=30,
                  text="My Planting Plan",
                  bg='dark green',
                  fg='white',
                  command=lambda: controller.show_frame(PlantingPlanReport)).grid(row=4,
                                                                                  column=2,
                                                                                  sticky='W')
        tk.Button(self,
                  width=30,
                  text="All Plants Detail",
                  bg='dark green',
                  fg='white',
                  command=lambda: controller.show_frame(PlantsDetailReport)
                  ).grid(row=4, column=3, sticky='E')

        tk.Button(self,
                  width=30,
                  text="Outcome Summary",
                  bg='dark green',
                  fg='white',
                  command=lambda: controller.show_frame(OutcomeSummaryReport)).grid(row=5,
                                                                                    column=2,
                                                                                    sticky='E')
        tk.Button(self,
                  width=30,
                  text="Outcome Detail",
                  bg='dark green',
                  fg='white',
                  command=lambda: controller.show_frame(OutcomeDetailReport)).grid(row=5,
                                                                                   column=3,
                                                                                   sticky='E')
        for child in self.winfo_children():
            child.grid_configure(padx=10,
                                 pady=10)


class PlantingPlanReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.set_labels(controller)

    def set_labels(self, controller):

        tk.Label(self,
                 text="Current Garden Plan",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  width=15,
                  text="Back to Reports",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(ReportsMenu)).grid(row=2,
                                                                           column=6)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')
        tk.Label(self,
                 text='Click "Refresh" to reflect changes: ',
                 anchor='e',
                 justify=tk.RIGHT,
                 font=MEDIUM_FONT,
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)
        tk.Button(self,
                  width=10,
                  text="Refresh",
                  anchor='center',
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.export_planting_plan(controller)).grid(row=3,
                                                                              column=3)
        tk.Button(self,
                  width=15,
                  text="Export (save) to CSV",
                  anchor='w',
                  justify=tk.LEFT,
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_planting_plan(controller)).grid(row=3,
                                                                              column=5)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)

        tk.Label(self,
                 text="Plant",
                 bg='white').grid(row=5,
                                   column=1)

        tk.Label(self,
                 text="Season",
                 bg='white').grid(row=5,
                                   column=2)

        tk.Label(self,
                 text="Zone",
                 bg='white').grid(row=5,
                                   column=3)

        tk.Label(self,
                 text="Plot",
                 bg='white').grid(row=5,
                                   column=4)

        tk.Label(self,
                 text=" Space / Seed Pack ",
                 bg='white').grid(row=5,
                                   column=5)

        tk.Label(self,
                 text=" Space / Seedling ",
                 bg='white').grid(row=5,
                                   column=6)

        tk.Label(self,
                 text=" Depth for Seeds ",
                 bg='white').grid(row=5,
                                   column=7)

        tk.Label(self,
                 text=" Watering Frequency ",
                 bg='white').grid(row=5,
                                   column=8)

        tk.Label(self,
                 text=" Days to Harvest ",
                 bg='white').grid(row=5,
                                   column=9)

        self.query_plan(controller)

    def reset_grid(self):
        for label in self.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def refresh_planting_plan(self, controller):
        self.reset_grid()
        self.set_labels(controller)
        self.query_plan(controller)

    def query_plan(self, controller):
        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(planting_plan_query)

            for row_number, row in enumerate(cursor, 6):
                tk.Label(self,
                         text=str(row[1]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[2]),
                         bg='white').grid(column=2,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[3]),
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[4]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[5]) + ' inches',
                         bg='white').grid(column=5,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[6]) + ' inches',
                         bg='white').grid(column=6,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[7]) + ' inches',
                         bg='white').grid(column=7,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[8]),
                         bg='white').grid(column=8,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[9]),
                         bg='white').grid(column=9,
                                          row=row_number)

            this_connection.end_connection()

        except:
            error_message = "Error displaying Planting Plan Report"
            controller.open_popup(controller,
                                  error_message)

    def export_planting_plan(self, controller):

        try:

            self.header = ["Season ID",
                           "Plant",
                           "Season",
                           "Zone",
                           "Plot Number",
                           "Space per Seed Pack",
                           "Space per Seedling",
                           "Depth to Plant Seeds",
                           "Watering Frequency",
                           "Days to Harvest"]

            new_export = export_query.ExportQuery()
            download_path = new_export.export_csv(planting_plan_query, self.header)

            success_message = "File Saved: " + download_path
            controller.open_popup(controller,
                                  success_message)

        except:
            error_message = "Error exporting Planting Plan Report"
            controller.open_popup(controller,
                                  error_message)


class PlantsDetailReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.set_labels(controller)

    def set_labels(self, controller):
        tk.Label(self,
                 text="All Available Plants",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  width=15,
                  text="Back to Reports",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(ReportsMenu)).grid(row=2,
                                                                           column=6)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Label(self,
                 text='Click "Refresh" to reflect changes: ',
                 anchor='e',
                 justify=tk.RIGHT,
                 font=MEDIUM_FONT,
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        tk.Button(self,
                  width=10,
                  text="Refresh",
                  anchor='center',
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.refresh_all_plants(controller)).grid(row=3,
                                                                            column=3)

        tk.Button(self,
                  width=15,
                  text="Export (save) to CSV",
                  anchor='w',
                  justify=tk.LEFT,
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.refresh_all_plants(controller)).grid(row=3,
                                                                            column=5)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)
        tk.Label(self,
                 text="Plant",
                 bg='white').grid(row=5,
                                   column=1)
        tk.Label(self,
                 text="In Plan?",
                 bg='white').grid(row=5,
                                   column=2)
        tk.Label(self,
                 text=" Crop Group ",
                 bg='white').grid(row=5,
                                   column=3)
        tk.Label(self,
                 text=" Sun Required ",
                 bg='white').grid(row=5,
                                   column=4)
        tk.Label(self,
                 text=" Soil Moisture ",
                 bg='white').grid(row=5,
                                   column=5)
        tk.Label(self,
                 text=" Space / Seed Pack ",
                 bg='white').grid(row=5,
                                   column=6)
        tk.Label(self,
                 text=" Space / Seedling ",
                 bg='white').grid(row=5,
                                   column=7)
        tk.Label(self,
                 text=" Depth Requirement ",
                 bg='white').grid(row=5,
                                   column=8)
        tk.Label(self,
                 text=" Watering Frequency ",
                 bg='white').grid(row=5,
                                   column=9)
        tk.Label(self,
                 text=" Frost Tolerance ",
                 bg='white').grid(row=5,
                                   column=10)
        tk.Label(self,
                 text=" Days to Harvest ",
                 bg='white').grid(row=5,
                                   column=11)
        tk.Label(self,
                 text="Plant in Spring?",
                 bg='white').grid(row=5,
                                   column=12)
        tk.Label(self,
                 text="Plant in Fall?",
                 bg='white').grid(row=5,
                                   column=13)
        self.query_all_plants(controller)

    def reset_grid(self):
        for label in self.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def refresh_all_plants(self, controller):
        self.reset_grid()
        self.set_labels(controller)
        self.query_all_plants(controller)

    def query_all_plants(self, controller):

        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(plant_detail_query)

            for row_number, row in enumerate(cursor, 6):
                tk.Label(self,
                         text=str(row[1]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[2]),
                         bg='white').grid(column=2,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[3]),
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[4]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[5]),
                         bg='white').grid(column=5,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[6]) + ' inches',
                         bg='white').grid(column=6,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[7]) + ' inches',
                         bg='white').grid(column=7,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[8]) + ' inches',
                         bg='white').grid(column=8,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[9]),
                         bg='white').grid(column=9,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[10]),
                         bg='white').grid(column=10,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[11]) + ' days',
                         bg='white').grid(column=11,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[12]),
                         bg='white').grid(column=12,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[13]),
                         bg='white').grid(column=13,
                                          row=row_number)

            this_connection.end_connection()

        except:
            error_message = "Error displaying Plant Detail Report"
            controller.open_popup(controller,
                                  error_message)

    def export_all_plants(self, controller):

        try:

            self.header = ["Plant ID",
                           "Plant Name",
                           "In Plan?",
                           "Crop Group",
                           "Sun Required",
                           "Soil Moisture Required",
                           "Space per Seed Pack",
                           "Space per Seedling",
                           "Depth Requirement",
                           "Watering Frequency",
                           "Frost Tolerance",
                           "Days to Harvest",
                           "Plant in Spring",
                           "Plant in Fall"]

            new_export = export_query.ExportQuery()
            download_path = new_export.export_csv(plant_detail_query, self.header)

            success_message = "File Saved: " + download_path
            controller.open_popup(controller,
                                  success_message)

        except:
            error_message = "Error exporting Plant Detail Report"
            controller.open_popup(controller,
                                  error_message)


class OutcomeDetailReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.set_labels(controller)

    def set_labels(self, controller):

        tk.Label(self,
                 text="Outcome Detail Report",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  width=15,
                  text="Back to Reports",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(ReportsMenu)).grid(row=2,
                                                                           column=6)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Label(self,
                 text='Click "Refresh" to reflect changes: ',
                 anchor='e',
                 justify=tk.RIGHT,
                 font=MEDIUM_FONT,
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        tk.Button(self,
                  width=10,
                  text="Refresh",
                  anchor='center',
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.refresh_outcome_detail(controller)).grid(row=3,
                                                                                column=3)

        tk.Button(self,
                  width=15,
                  text="Export (save) to CSV",
                  anchor='w',
                  justify=tk.LEFT,
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_outcome_detail(controller)).grid(row=3,
                                                                               column=5)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)
        tk.Label(self,
                 text="Plant Set ID",
                 bg='white').grid(row=5,
                                   column=1)
        tk.Label(self,
                 text="Season",
                 bg='white').grid(row=5,
                                   column=2)
        tk.Label(self,
                 text="Plant",
                 bg='white').grid(row=5,
                                   column=3)
        tk.Label(self,
                 text="Zone",
                 bg='white').grid(row=5,
                                   column=4)
        tk.Label(self,
                 text="Plot",
                 bg='white').grid(row=5,
                                   column=5)
        tk.Label(self,
                 text=" Set Quantity ",
                 bg='white').grid(row=5,
                                   column=6)
        tk.Label(self,
                 text=" Set Type ",
                 bg='white').grid(row=5,
                                   column=7)
        tk.Label(self,
                 text=" Date Planted ",
                 bg='white').grid(row=5,
                                   column=8)
        tk.Label(self,
                 text=" First Harvest ",
                 bg='white').grid(row=5,
                                   column=9)
        tk.Label(self,
                 text=" Last Harvest ",
                 bg='white').grid(row=5,
                                   column=10)
        tk.Label(self,
                 text="Outcome",
                 bg='white').grid(row=5,
                                   column=11)

        self.query_outcome_detail(controller)

    def reset_grid(self):
        for label in self.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def refresh_outcome_detail(self, controller):
        self.reset_grid()
        self.set_labels(controller)
        self.query_outcome_detail(controller)

    def query_outcome_detail(self, controller):

        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(outcome_detail_query)

            for row_number, row in enumerate(cursor, 6):
                tk.Label(self,
                         text=str(row[0]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[1]),
                         bg='white').grid(column=2,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[2]),
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[3]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[4]),
                         bg='white').grid(column=5,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[5]),
                         bg='white').grid(column=6,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[6]),
                         bg='white').grid(column=7,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[7]),
                         bg='white').grid(column=8,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[8]),
                         bg='white').grid(column=9,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[9]),
                         bg='white').grid(column=10,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[10]),
                         bg='white').grid(column=11,
                                          row=row_number)

            this_connection.end_connection()

        except:
            error_message = "Error displaying Outcome Detail Report"
            controller.open_popup(controller,
                                  error_message)

    def export_outcome_detail(self, controller):

        try:
            self.header = ["Plant Set ID",
                           "Season",
                           "Plant",
                           "Zone",
                           "Plot Number",
                           "Set Quantity",
                           "Set Type",
                           "Date Planted",
                           "First Harvest",
                           "Last Harvest",
                           "Outcome"]

            new_export = export_query.ExportQuery()
            download_path = new_export.export_csv(outcome_detail_query, self.header)

            success_message = "File Saved: " + download_path
            controller.open_popup(controller,
                                  success_message)
        except:
            error_message = "Error exporting Outcome Detail Report"
            controller.open_popup(controller,
                                  error_message)


class OutcomeSummaryReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.set_labels(controller)

    def set_labels(self, controller):

        tk.Label(self,
                 text="Outcome Summary Report",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=8,
                                                                         sticky='EW')

        tk.Button(self,
                  width=15,
                  text="Back to Reports",
                  bg='white',
                  fg='dark red',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(ReportsMenu)).grid(row=2,
                                                                           column=5)

        tk.Label(self,
                 text='Click "Refresh" to reflect changes: ',
                 anchor='e',
                 justify=tk.RIGHT,
                 font=MEDIUM_FONT,
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        tk.Button(self,
                  width=10,
                  text="Refresh",
                  anchor='center',
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.refresh_outcome_summary(controller)).grid(row=3,
                                                                                 column=3)

        tk.Button(self,
                  width=15,
                  text="Export (save) to CSV",
                  anchor='w',
                  justify=tk.LEFT,
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_outcome_summary(controller)).grid(row=3,
                                                                                column=4)

        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)

        tk.Label(self,
                 text="Plant Name",
                 bg='white').grid(row=5,
                                   column=1)

        tk.Label(self,
                 text=" Times Planted ",
                 bg='white').grid(row=5,
                                   column=2)

        tk.Label(self,
                 text=" Success Ratio ",
                 bg='white').grid(row=5,
                                   column=3)

        tk.Label(self,
                 text=" Most Recent Season ",
                 bg='white').grid(row=5,
                                   column=4)

        tk.Label(self,
                 text=" Most Recent Outcome ",
                 bg='white').grid(row=5,
                                   column=5)

        self.query_outcome_summary(controller)

    def reset_grid(self):
        for label in self.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def refresh_outcome_summary(self, controller):
        self.reset_grid()
        self.set_labels(controller)
        self.query_outcome_summary(controller)

    def query_outcome_summary(self, controller):

        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(outcome_summary_query)

            for row_number, row in enumerate(cursor, 6):
                tk.Label(self,
                         text=str(row[0]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[1]),
                         bg='white').grid(column=2,
                                          row=row_number)
                if row[2] is None:
                    ratio_text = 'N/A'
                else:
                    ratio_text = str(row[2]) + '%'

                tk.Label(self,
                         text=ratio_text,
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[3]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[4]),
                         bg='white').grid(column=5,
                                          row=row_number)

            this_connection.end_connection()


        except:
            error_message = "Error displaying Outcome Summary Report"
            controller.open_popup(controller,
                                  error_message)

    def export_outcome_summary(self, controller):

        try:

            self.header = ["Plant Name",
                           "Times Planted",
                           "Success Ratio",
                           "Most Recent Season",
                           "Most Recent Outcome"]

            new_export = export_query.ExportQuery()
            download_path = new_export.export_csv(outcome_summary_query, self.header)

            success_message = "File Saved: " + download_path
            controller.open_popup(controller,
                                  success_message)

        except:
            error_message = "Error exporting Outcome Summary Report"
            controller.open_popup(controller,
                                  error_message)


class CompleteYearPage(tk.Frame):

    def __init__(self,
                 parent,
                 controller):
        tk.Frame.__init__(self,
                          parent)

        self.plant_set_list = []

        self.set_default_values()

        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=2,
                                                                         column=9,
                                                                         sticky='EW')

        tk.Button(self,
                  width=5,
                  text="Go",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.import_values(controller)).grid(row=3,
                                                                       column=5,
                                                                       sticky='E')

        tk.Button(self,
                  width=15,
                  text="Complete",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.complete_seasons(controller)).grid(row=3,
                                                                          column=9,
                                                                          sticky='E')
        # set default value for spinbox to last year
        current_date = date.today()
        last_year = current_date.year - 1
        self.year_spinbox = tk.Spinbox(self,
                                       from_=last_year,
                                       to=3000,
                                       width=10)
        self.year_spinbox.grid(row=3,
                               column=4)

    # set values that display when the window first loads

    def set_default_values(self):
        tk.Label(self,
                 text="Complete Year",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Label(self,
                 text="Select Year to Finalize:",
                 font=MEDIUM_FONT,
                 justify=tk.RIGHT,
                 anchor='e',
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=3)
        tk.Label(self,
                 text="",
                 bg='white').grid(row=4,
                                  column=2)
        tk.Label(self,
                 text="Season",
                 bg='white').grid(row=5,
                                  column=1)
        tk.Label(self,
                 text="Plant Set ID",
                 bg='white').grid(row=5,
                                  column=2)
        tk.Label(self,
                 text="Plant",
                 bg='white').grid(row=5,
                                  column=3)
        tk.Label(self,
                 text="Zone",
                 bg='white').grid(row=5,
                                  column=4)
        tk.Label(self,
                 text="Plot Number",
                 bg='white').grid(row=5,
                                  column=5)
        tk.Label(self,
                 text="Date Planted",
                 bg='white').grid(row=5,
                                  column=6)
        tk.Label(self,
                 text="Last Harvest",
                 bg='white').grid(row=5,
                                  column=7)
        tk.Label(self,
                 text="Outcome",
                 bg='white').grid(row=5,
                                  column=8)
        tk.Label(self,
                 text="Season Active",
                 bg='white').grid(row=5,
                                  column=9)

    def import_values(self, controller):
        try:
            self.closeout_year = planting_year.PlantingYear()
            self.closeout_year.my_year = self.year_spinbox.get()

            print("closeout year = " + str(self.closeout_year.my_year))

            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            (cursor.execute(year_data_query + ' ?', [self.closeout_year.my_year]))

            for row_number, row in enumerate(cursor, 6):

                if row[10] is None:
                    outcome = "TBD"
                elif row[10] is True:
                    outcome = "Success"
                else:
                    outcome = "Failure"

                if row[11] is True:
                    active_status = "Yes"
                else:
                    active_status = "No"

                tk.Label(self,
                         text=str(row[2]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[3]),
                         bg='white').grid(column=2,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[4]),
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[6]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[7]),
                         bg='white').grid(column=5,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[8]),
                         bg='white').grid(column=6,
                                          row=row_number)
                tk.Label(self,
                         text=str(row[9]),
                         bg='white').grid(column=7,
                                          row=row_number)
                tk.Label(self,
                         text=outcome,
                         bg='white').grid(column=8,
                                          row=row_number)
                tk.Label(self,
                         text=active_status,
                         bg='white').grid(column=9,
                                          row=row_number)

                self.complete_plant_set = plant_set.PlantSet()

                # 0 values are placeholders, not being used
                self.complete_plant_set.add_new_plant_set(row[5], 0, 0)
                self.complete_plant_set.add_plot_id(row[7])
                self.complete_plant_set.add_season_id(row[1])
                self.complete_plant_set.outcome = row[10]

                self.plant_set_list.append(self.complete_plant_set)

            this_connection.end_connection()

            tk.Label(self,
                     text=" ",
                     bg='white').grid(row=row_number + 1,
                                      column=2)

        except:
            error_message = "Invalid year, please try again."
            controller.open_popup(controller,
                                  error_message)

    def complete_seasons(self, controller):

        try:
            self.closeout_year.complete_planting_year(self.plant_set_list)
            success_message = "Year completed successfully!"
            controller.open_popup(controller,
                                  success_message)

        except:
            error_message = "Error completing year."
            controller.open_popup(controller,
                                  error_message)


app = Window()
app.mainloop()
