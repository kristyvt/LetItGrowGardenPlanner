'''
Let it Grow Garden Planner
Garden planning and outcome tracking tool
Kristy Stark
Champlain College SDEV-435-81

Window runs the interface and calls
associated classes to run program.
Last Revised 8/3/24
'''

# built in libraries
import os  # to locate file path for images
import sys  # for system exit
import tkinter as tk  # interface and formatting libraries
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date, datetime

# custom task handling libraries
import data_connection  # manages connection to server
import validate  # manages all data validation
import export_query  # exports report data to CSV

# custom class objects
import my_season
import plan
import plant
import plant_set
import planting_year
import plot

# Font Styles
LARGE_FONT = ("Helvetica", 16, 'bold')
MEDIUM_FONT = ("Helvetica", 12)

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


# Class to manage all dropdown lists
class DropDown:
    def __init__(self,
                 parent,
                 query_name,
                 row,
                 column,
                 column_span,
                 sticky):
        try:
            # establish connection to database

            self.this_connection = data_connection.Connection()
            self.cursor = self.this_connection.connection.cursor()

            # create list to store dropdown values
            # and variables to store selection and corresponding database ID

            self.drop_down_list = []
            self.selection = None
            self.id = None

            # Execute the SQL query to retrieve the dropdown values
            # Any SQL query with first two columns as ID, Value can be used

            self.cursor.execute(query_name)
            records = self.cursor.fetchall()
            for r in records:
                drop_down_value = r[1]

                # don't add repeat values to the list
                if drop_down_value in self.drop_down_list:
                    continue
                else:
                    # add all new values to dropdown list
                    self.drop_down_list.append(drop_down_value)

            # Create dropdown containing values from list
            # and place per parameters passed

            self.combo = ttk.Combobox(parent,
                                      values=self.drop_down_list)
            self.combo.grid(row=row,
                            column=column,
                            columnspan=column_span,
                            sticky=sticky)

            # call function to retrieve value when item is selected
            self.combo.set('Select Value')
            self.combo.bind('<<ComboboxSelected>>',
                            self.get_value)
        except:
            print("no connection dropdown")

    # Function to retrieve value selected from dropdown list
    # "Event" parameter is necessary to bind value to action,
    #  even though it doesn't appear in the function itself.
    def get_value(self,
                  event):

        # get value selected and set as selection
        self.selection = self.combo.get()

    # function to retrieve the database ID of the dropdown item selected
    def get_id(self,
               query_name,
               value):
        this_connection = data_connection.Connection()  # connect to server
        cursor = this_connection.connection.cursor()  # set connection cursor

        # This program uses same query as the that to populate dropdown
        # But any SQL query with first two columns as ID, Value will work

        cursor.execute(query_name)
        records = cursor.fetchall()
        for r in records:
            if value == r[1]:
                # when the value the user selected is found
                # set the id variable to the ID of the value found
                # then end connection and return ID to calling function

                self.id = r[0]
                this_connection.end_connection()
                return self.id


# Class to manage all interface windows
# All windows are generated from this class
# so are generated when this class is called upon startup.

class Window(tk.Tk):

    def __init__(self,
                 *args,
                 **kwargs):
        tk.Tk.__init__(self,
                       *args,
                       **kwargs)
        self.geometry("1250x500")
        self.configure(bg='white')
        container = tk.Frame(self)
        container.configure(bg='white')

        # title appearing at the top of all primary windows
        self.title("Let it Grow Garden Planner")

        # icon in the top left corner
        icon_file = "Icon.png"
        icon_folder = "Images"
        # set file path for logo file location
        path = os.path.abspath(__file__)
        icon_dir = os.path.dirname(path)
        icon_path = os.path.join(icon_dir, icon_folder, icon_file)

        img = tk.PhotoImage(file=icon_path)
        self.iconphoto(False, img)


        # set default layout for interface windows

        container.pack()
        container.grid_rowconfigure(0,
                                    weight=1)
        container.grid_columnconfigure(0,
                                       weight=1)

        test_connection = data_connection.Connection()
        if test_connection.status == "success":

            # create a dictionary of frames
            # each frame is a primary window

            self.frames = {}

            # generate the dictionary of frames
            # each frame is a class

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
                      CompleteYearPage):
                frame = F(container,
                          self)

                self.frames[F] = frame

            # set initial window as the start page
            self.show_frame(StartPage)
        else:
            # create a dictionary of frames
            # each frame is a primary window

            self.frames = {}

            # generate the dictionary of frames
            # each frame is a class

            for F in (StartPage,):
                frame = F(container,
                          self)

                self.frames[F] = frame

            # set initial window as the start page
            self.show_frame(StartPage)
            self.open_popup(self, "Database does not exist."
                                  "\nPlease install Garden database and try again")

    # function to display a selected frame
    # generally used with buttons
    def show_frame(self, cont):
        frame = self.frames[cont]
        # set background color
        frame.configure(bg='white')
        frame.grid(row=0,
                   column=0,
                   sticky="nsew",
                   padx=25,
                   pady=25)
        frame.tkraise()

    # function to close the window which exits the program
    def close_window(self):
        sys.exit(0)

    # function to close only a popup window while leaving primary window open
    def close_popup(self, top):
        top.destroy()

    # function to open a new window that displays a message
    # generally used for confirmation and error messages
    def open_popup(self, controller, message):
        # set formatting for just this window
        top = tk.Toplevel(self)
        top.geometry("400x200")
        top.configure(bg='white',
                      padx=25,
                      pady=25)

        # set title for just this window
        top.title("Notification")


        # icon in the top left corner
        icon_file = "Icon.png"
        icon_folder = "Images"
        # set file path for logo file location
        path = os.path.abspath(__file__)
        icon_dir = os.path.dirname(path)
        icon_path = os.path.join(icon_dir, icon_folder, icon_file)

        img = tk.PhotoImage(file=icon_path)
        top.iconphoto(False, img)

        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=1,
                                  column=1,
                                  sticky="nsew")

        # print message passed by calling function
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

        # explicitly close popup window only
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
        logo_folder = "Images"

        # set file path for logo file location
        path = os.path.abspath(__file__)
        logo_dir = os.path.dirname(path)
        logo_path = os.path.join(logo_dir,logo_folder, logo_file)

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
                  text="Create Garden Plan",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(GardenPlanPage)).grid(row=3,
                                                                              column=2,
                                                                              sticky='E')
        tk.Button(self,
                  width=20,
                  text="Complete Year",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(CompleteYearPage)).grid(row=3,
                                                                                column=3,
                                                                                sticky='EW')
        tk.Button(self,
                  width=25,
                  text="View Garden Plan",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.show_frame(DisplayPlan)).grid(row=4,
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
                  text="Exit",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 12',
                  command=lambda: controller.close_window()).grid(row=4,
                                                                  column=3,
                                                                  sticky='E')
        tk.Label(self,
                 text='Brand new? Click "Garden Setup & Maintenance" to create your Garden.',
                 font=MEDIUM_FONT,
                 fg='dark green',
                 bg='white').grid(row=6,
                                  column=1,
                                  columnspan=3)
        tk.Label(self,
                 text='Then click "Create Garden Plan" to select which Plants to grow!',
                 font=MEDIUM_FONT,
                 fg='dark green',
                 bg='white').grid(row=7,
                                  column=1,
                                  columnspan=3)

        tk.Label(self,
                 text='Is the year over? Update the plot statuses by clicking "Complete Year."',
                 justify=tk.LEFT,
                 anchor='w',
                 bg='white',
                 fg='dark green',
                 font=MEDIUM_FONT).grid(row=8,
                                        column=1,
                                        columnspan=3)

        for child in self.winfo_children():
            child.grid_configure(padx=10,
                                 pady=10)


# class to add a new plant to the master list

class AddPlantPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # launch window

        tk.Label(self,
                 text="Add New Plant",
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
                 text="Depth to Plant Seeds, in inches, will round to 2 decimal places (optional):",
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
                 text="Days to Harvest (optional):",
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

        # create plant object to store plant details selected by user    # CHECK IF THIS IS NECESSARY IN TESTING
        self.new_plant = plant.Plant()

        # button captures user inputs and selections as of when button is pressed
        tk.Button(self,
                  text="Add Plant",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  width=15,
                  command=lambda: self.add_new_plant(controller)).grid(row=12,
                                                                       column=8)

    # function to retrieve user inputs and selections
    # set variables stored in plant object
    # and pass them to the function to export to database
    def add_new_plant(self, controller):

        self.space_required_seedling = None
        self.space_required_seeds = None
        self.depth_requirement = None
        self.depth_to_plant_seeds = None
        self.days_to_harvest = None

        try:

            # set variables to values input onscreen
            # after data validation of each

            # get and validate plant name entry

            data_to_validate = validate.Validate(self.plant_name_entry.get())
            if data_to_validate.validate_text():
                self.plant_name = self.plant_name_entry.get()

            elif data_to_validate.validate_text() is False:
                error_message = ("Invalid Plant Name entered"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                error_message = ("No Plant Name entered"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # set to None so that either can be blank
            self.plant_in_spring = None
            self.plant_in_fall = None

            # check that at least one season selection was made
            self.plant_in_spring = bool(self.plant_spring.get())
            self.plant_in_fall = bool(self.plant_fall.get())

            # error if neither season was checked
            if self.plant_in_spring is False and self.plant_in_fall is False:
                error_message = ("Missing Spring or Fall selection"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # get and validate crop group entry

            data_to_validate = validate.Validate(self.crop_group_combo.selection)
            if data_to_validate.validate_text():
                crop_group_text = self.crop_group_combo.selection
                self.crop_group_id = int(self.crop_group_combo.get_id(crop_group_query,
                                                                      crop_group_text))

            elif data_to_validate.validate_text() is False:
                error_message = ("Invalid or missing Crop Group entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                error_message = ("Invalid or missing Crop Group entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # get and validate sun requirement entry

            data_to_validate = validate.Validate(self.sun_combo.selection)
            if data_to_validate.validate_text():
                sun_id_text = self.sun_combo.selection
                self.sun_id = int(self.sun_combo.get_id(sun_query,
                                                        sun_id_text))

            elif data_to_validate.validate_text() is False:
                error_message = ("Invalid or missing Sun entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                error_message = ("Invalid or missing Sun entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # get and validate frost tolerance entry

            data_to_validate = validate.Validate(self.frost_tolerance_combo.selection)
            if data_to_validate.validate_text():
                frost_tolerance_text = self.frost_tolerance_combo.selection
                self.frost_tolerance_id = \
                    int(self.frost_tolerance_combo.get_id(frost_tolerance_query,
                                                          frost_tolerance_text))

            elif data_to_validate.validate_text() is False:
                error_message = ("Invalid or missing Frost Tolerance entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                error_message = ("Invalid or missing Frost Tolerance entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # get and validate soil moisture requirement entry

            data_to_validate = validate.Validate(self.soil_moisture_combo.selection)
            if data_to_validate.validate_text():
                soil_moisture_text = self.soil_moisture_combo.selection
                self.soil_moisture_id = \
                    int(self.soil_moisture_combo.get_id(soil_moisture_query,
                                                        soil_moisture_text))

            elif data_to_validate.validate_text() is False:
                error_message = ("Invalid or missing Soil Moisture entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                error_message = ("Invalid or missing Soil Moisture entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # get and validate space required for seedling entry

            space_required_seedling = self.space_per_seedling_entry.get()

            if space_required_seedling == "" or space_required_seedling is None:
                print('No seedling spacing entered')
                error_message = ("Missing or invalid seedling spacing selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                test_space_required_seedling = validate.Validate(space_required_seedling)
                if test_space_required_seedling.validate_positive_int():
                    print('seedling spacing validation passed')
                    self.space_required_seedling = int(space_required_seedling)
                else:
                    error_message = ("Missing or invalid seedling spacing selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # get and validate space required for seeds entry

            space_required_seeds = self.space_per_seedpack_entry.get()

            if space_required_seeds == "" or space_required_seeds is None:
                print('No seed spacing entered')
                error_message = ("Missing or invalid seed spacing selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                test_space_required_seeds = validate.Validate(space_required_seeds)
                if test_space_required_seeds.validate_positive_int():
                    print('seed spacing validation passed')
                    self.space_required_seeds = int(space_required_seeds)
                else:
                    error_message = ("Missing or invalid seed spacing selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

                # get and validate depth requirement entry

                depth_requirement = self.depth_per_plant_entry.get()

                if depth_requirement == "" or depth_requirement is None:
                    print('No depth_requirement entered')
                    error_message = ("Missing or invalid depth requirement."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError
                else:
                    test_depth_requirement = validate.Validate(depth_requirement)
                    if test_depth_requirement.validate_positive_int():
                        print('depth_requirement validation passed')
                        self.depth_requirement = int(depth_requirement)
                    else:
                        error_message = ("Missing or invalid depth requirement."
                                         "\nPlease try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

                # get and validate depth to plant seeds entry

                depth_to_plant_seeds = self.depth_for_seeds_entry.get()

                # do nothing if blank, can be null
                if depth_to_plant_seeds == "" or depth_to_plant_seeds is None:
                    print('No depth to plant seeds entered')

                # run validation test
                else:
                    test_depth_to_plant_seeds = validate.Validate(depth_to_plant_seeds)
                    if test_depth_to_plant_seeds.validate_positive_float():
                        print('depth to plant seeds validation passed')
                        self.depth_to_plant_seeds = float(depth_to_plant_seeds)
                        self.depth_to_plant_seeds = round(self.depth_to_plant_seeds, 2)
                    else:
                        error_message = ("Invalid Depth to Plant Seeds."
                                         "\nPlease try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

                # get and validate days to harvest entry

                days_to_harvest = self.days_to_harvest_entry.get()

                # do nothing if blank, can be null
                if days_to_harvest == "" or days_to_harvest is None:
                    print('No days to harvest entered')

                # run validation test
                else:
                    test_days_to_harvest = validate.Validate(days_to_harvest)
                    if test_days_to_harvest.validate_positive_int():
                        print('days to harvest validation passed')
                        self.days_to_harvest = int(days_to_harvest)
                    else:
                        error_message = ("Invalid Days to Harvest."
                                         "\nPlease try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

            # get and validate watering requirement entry

            data_to_validate = validate.Validate(self.watering_requirement_combo.selection)
            if data_to_validate.validate_text():
                watering_requirement_text = self.watering_requirement_combo.selection
                self.watering_requirement_id = \
                    int(self.watering_requirement_combo.get_id(watering_requirement_query,
                                                               watering_requirement_text))

            elif data_to_validate.validate_text() is False:
                error_message = ("Invalid or missing Watering Requirement entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                error_message = ("Invalid or missing Watering Requirement entry"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

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
                error_message = ("Error inserting into database"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)

        # exception handling for invalid data entry
        except ValueError:
            pass
        except Exception:
            error_message = ("Other error"
                             "\nNew plant not added.")
            controller.open_popup(controller,
                                  error_message)


# class to create new planting instances, or plant sets
# and add them to a new plan automatically or manually
class GardenPlanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,
                          parent)

        self.set_default_values(controller)

    def set_default_values(self, controller):

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
                 text="Click Refresh to reflect recent changes",
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
                  command=lambda: self.set_default_values(controller)).grid(row=5,
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
                                  columnspan=4)

        # setup spinbox with the highest plot ID number as max value
        self.plot_stat_list = []
        top_plot_id = 1
        top_zone_id = 1
        top_row = 1
        top_column = 1

        try:

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

    def validate_plant_selection(self, controller):

        plant = self.plant_combo.selection

        if plant == "" or plant is None:
            print('No plant entered')
            error_message = ("Missing or invalid Plant Name selection."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_plant = validate.Validate(self.plant_combo.selection)
            if test_plant.validate_text():
                print('Plant selection validation passed')
                plant = self.plant_combo.selection
                return plant

            else:
                error_message = ("Missing or invalid Plant Name selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_season_selection(self, controller):

        season = self.season_combo.selection

        if season == "" or season is None:
            print('No season entered')
            error_message = ("Missing or invalid season selection."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_season = validate.Validate(self.season_combo.selection)
            if test_season.validate_text():
                print('season selection validation passed')
                season = self.season_combo.selection
                return season

            else:
                error_message = ("Missing or invalid season selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_set_type_selection(self, controller):

        set_type = self.set_type_combo.selection

        if set_type == "" or set_type is None:
            print('No set_type entered')
            error_message = ("Missing or invalid Set Type."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_set_type = validate.Validate(set_type)
            if test_set_type.validate_text():
                print('set_type selection validation passed')
                set_type = set_type
                return set_type

            else:
                error_message = ("Missing or invalid Set Type selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_plot_selection(self, controller):

        plot = self.plot_spinbox.get()

        if plot == "" or plot is None or plot == '0':
            print('No plot entered')
            return None

        else:
            test_plot = validate.Validate(plot)
            if test_plot.validate_positive_int():
                print('plot selection validation passed')
                plot = plot
                return plot

            else:
                error_message = ("Invalid Plot selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_set_quantity_selection(self, controller):

        set_quantity = self.quantity_entry.get()

        if set_quantity == "" or set_quantity is None:
            print('No set_type entered')
            error_message = ("Missing or invalid Set Quantity."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_plot = validate.Validate(set_quantity)
            if test_plot.validate_positive_int():
                print('set_quantity selection validation passed')
                set_quantity = set_quantity
                return set_quantity

            else:
                error_message = ("Missing or invalid Set Quantity."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def add(self, controller):
        self.set_quantity = None
        self.plant_id = None
        self.my_season_id = None
        self.plot_id = None
        self.set_type_id = None

        try:

            # get and validate plant selection
            validated_plant = self.validate_plant_selection(controller)
            if validated_plant:
                self.plant_id = int(self.plant_combo.get_id(plant_name_query,
                                                            validated_plant))
                print('Plant ID selected is: ' + str(self.plant_id))
            else:
                print('No Plant ID')
                raise ValueError

            # get and validate set type selection
            validated_set_type = self.validate_set_type_selection(controller)
            if validated_set_type:
                self.set_type_id = int(self.set_type_combo.get_id(set_type_query,
                                                                  validated_set_type))
                print("Set Type ID is " + str(self.set_type_id))

            else:
                print('No Set Type ID')
                raise ValueError

            # get and validate set quantity entered
            validated_quantity = self.validate_set_quantity_selection(controller)
            if validated_quantity:
                self.set_quantity = validated_quantity
                print('set quantity is ' + str(self.set_quantity))
            else:
                raise ValueError

            self.new_plant_set = plant_set.PlantSet()
            self.new_plant_set.add_new_plant_set(self.plant_id,
                                                 self.set_type_id,
                                                 self.set_quantity)

            self.new_plan.plant_set_list.append(self.new_plant_set)

            success_message = (str(self.set_quantity)
                               + " " + validated_set_type
                               + " of " + validated_plant
                               + "\nadded to tentative Garden Plan.")

            controller.open_popup(controller,
                                  success_message)

        except ValueError:
            pass
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
            error_message = ("No plants listed in tentative Garden Plan.\n"
                             "Please add at least one Plant to Auto-Plan.")
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

            # get and validate plant selection
            validated_plant = self.validate_plant_selection(controller)
            if validated_plant:
                self.plant_id = int(self.plant_combo.get_id(plant_name_query,
                                                            validated_plant))
                print('Plant ID selected is: ' + str(self.plant_id))
            else:
                print('No Plant ID')
                raise ValueError

            # get and validate set type selection
            validated_set_type = self.validate_set_type_selection(controller)
            if validated_set_type:
                self.set_type_id = int(self.set_type_combo.get_id(set_type_query,
                                                                  validated_set_type))
                print("Set Type ID is " + str(self.set_type_id))

            else:
                print('No Set Type ID')
                raise ValueError

            # get and validate set quantity entered
            validated_quantity = self.validate_set_quantity_selection(controller)
            if validated_quantity:
                self.set_quantity = validated_quantity
                print('set quantity is ' + str(self.set_quantity))
            else:
                raise ValueError

            # get and validate season selection
            validated_season = self.validate_season_selection(controller)
            if validated_season:
                self.my_season_id = int(self.season_combo.get_id(seasons_query,
                                                                 validated_season))
                print("season ID is " + str(self.my_season_id))
            else:
                raise ValueError

            # get and validate plot entered
            validated_plot = self.validate_plot_selection(controller)

            if validated_plot:
                self.set_plot_id = validated_plot
                print('plot is ' + str(self.set_plot_id))
            else:

                zone = self.zone_combo.combo.get()

                if zone == "" or zone is None:
                    print('No zone or plot entered')
                    error_message = ("Missing Zone or Plot selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

                else:
                    test_zone = validate.Validate(zone)
                    if test_zone.validate_text():
                        print('Zone selection validation passed')
                        self.zone_id = int(self.zone_combo.get_id(zone_query,
                                                              zone))

                    else:
                        error_message = ("Invalid Zone selection."
                                         "\nPlease try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

                # get and validate row entry

                row = self.row_spinbox.get()

                if row == "" or row is None or row == '0':
                    print('No Row or Plot entered')
                    error_message = ("Missing Row or Plot selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

                # run validation test
                else:
                    test_row = validate.Validate(row)
                    if test_row.validate_positive_int():
                        print('row validation passed')
                        self.row = row
                    else:
                        error_message = ("Invalid Row entry."
                                         "\nPlease try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

                # get and validate column entry

                column = self.col_spinbox.get()

                if column == "" or column is None or column == '0':
                    print('No Column or Plot entered')
                    error_message = ("Missing Column or Plot selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

                # run validation test
                else:
                    test_column = validate.Validate(column)
                    if test_column.validate_positive_int():
                        print('row validation passed')
                        self.column = column
                    else:
                        error_message = ("Invalid Column entry."
                                         "\nPlease try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

            self.new_plant_set = plant_set.PlantSet()
            print('plant ID is ' + str(self.plant_id))
            self.new_plant_set.add_new_plant_set(self.plant_id,
                                                 self.set_type_id,
                                                 self.set_quantity)
            print('manual plan interface zone id ' + str(self.zone_id))

            this_manual_plan = plan.Plan()
            message = this_manual_plan.manual_plan(self.new_plant_set,
                                                   self.my_season_id,
                                                   self.set_plot_id,
                                                   self.zone_id,
                                                   self.row,
                                                   self.column)

            controller.open_popup(controller, message)

        except ValueError:
            pass
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
                 text="Update Plant Set",
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
                 font=MEDIUM_FONT).grid(row=3,
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

        # start "date planted" label and date entry

        tk.Label(self,
                 text="Date Planted:",
                 bg='white').grid(row=7,
                                  column=6,
                                  columnspan=1)

        self.date_planted_entry = DateEntry(self,
                                            width=10,
                                            background="green",
                                            foreground="white",
                                            bd=2)
        self.date_planted_entry.grid(row=7,
                                     column=7)

        # clear date entry so that it's blank instead of current date
        self.date_planted_entry.delete(0, 'end')

        # end "date planted" label and date entry
        # start "first harvest date" label and date entry

        tk.Label(self,
                 text="First Harvest Date:",
                 bg='white').grid(row=8,
                                  column=6,
                                  columnspan=1)
        self.first_harvest_entry = DateEntry(self,
                                             width=10,
                                             background="green",
                                             foreground="white",
                                             bd=2)
        self.first_harvest_entry.grid(row=8,
                                      column=7)
        self.first_harvest_entry.delete(0, 'end')

        # end "first harvest date" label and date entry
        # start "last harvest date" label and date entry

        tk.Label(self,
                 text="Last Harvest Date:",
                 bg='white').grid(row=9,
                                  column=6,
                                  columnspan=1)
        self.last_harvest_entry = DateEntry(self,
                                            width=10,
                                            background="green",
                                            foreground="white",
                                            bd=2)
        self.last_harvest_entry.grid(row=9,
                                     column=7)

        self.last_harvest_entry.delete(0, 'end')

        # end "last harvest date" label and date entry

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

    def validate_plant_selection(self, controller):

        plant = self.plant_combo.selection

        if plant == "" or plant is None:
            print('No plant entered')
            error_message = ("Missing or invalid Plant Name selection."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_plant = validate.Validate(self.plant_combo.selection)
            if test_plant.validate_text():
                print('Plant selection validation passed')
                plant = self.plant_combo.selection
                return plant

            else:
                error_message = ("Missing or invalid Plant Name selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_season_selection(self, controller):

        season = self.season_combo.selection

        if season == "" or season is None:
            print('No season entered')
            error_message = ("Missing or invalid season selection."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_season = validate.Validate(self.season_combo.selection)
            if test_season.validate_text():
                print('season selection validation passed')
                season = self.season_combo.selection
                return season

            else:
                error_message = ("Missing or invalid season selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_set_type_selection(self, controller):

        set_type = self.set_type_combo.selection

        if set_type == "" or set_type is None:
            print('No set_type entered')
            error_message = ("Missing or invalid Set Type."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_set_type = validate.Validate(set_type)
            if test_set_type.validate_text():
                print('set_type selection validation passed')
                set_type = set_type
                return set_type

            else:
                error_message = ("Missing or invalid Set Type selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_plot_selection(self, controller):

        plot = self.plot_entry.get()

        if plot == "" or plot is None:
            print('No plot entered')
            error_message = ("Missing or invalid Plot selection."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_plot = validate.Validate(plot)
            if test_plot.validate_positive_int():
                print('plot selection validation passed')
                plot = plot
                return plot

            else:
                error_message = ("Missing or invalid Plot selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_set_quantity_selection(self, controller):

        set_quantity = self.quantity_entry.get()

        if set_quantity == "" or set_quantity is None:
            print('No set_type entered')
            error_message = ("Missing or invalid Set Quantity."
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

        else:
            test_plot = validate.Validate(set_quantity)
            if test_plot.validate_positive_int():
                print('set_quantity selection validation passed')
                set_quantity = set_quantity
                return set_quantity

            else:
                error_message = ("Missing or invalid Set Quantity."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

    def validate_notes_entry(self, controller):

        set_notes = self.set_notes_text.get(1.0, 'end')
        print(set_notes)

        if set_notes.strip() == "" or set_notes.strip() is None:
            return None

        test_notes = validate.Validate(set_notes.strip())
        if test_notes.validate_text():
            print('notes selection validation passed')
            set_notes = set_notes
            return set_notes

        else:
            error_message = ("Invalid Notes entry."
                             "\nAllowed special characters are: -_',:%&()"
                             "\nPlease try again.")
            controller.open_popup(controller,
                                  error_message)
            raise ValueError

    def import_plant_set(self, controller):

        try:

            self.saved_plant_set = plant_set.PlantSet()

            # begin getting and validating plant selection

            validated_plant = self.validate_plant_selection(controller)
            if validated_plant:
                plant_selection = self.plant_combo.selection
            else:
                raise ValueError

            # end getting and validating plant selection

            # begin getting and validating season selection

            validated_season = self.validate_season_selection(controller)
            if validated_season:
                season_selection = self.season_combo.selection
            else:
                raise ValueError

            # end getting and validating season selection

            # start search at plant set ID 0
            set_to_check = 0

            # search for the first plant ID matching the plant name and season

            q_plant_set_id = self.saved_plant_set.import_plant_set(plant_selection,
                                                                   season_selection,
                                                                   set_to_check)
            if q_plant_set_id is None and set_to_check == 0:

                error_text = "Plant Not Found"
                controller.open_popup(controller, error_text)

                self.set_default_values(controller)

            elif q_plant_set_id is None and set_to_check > 0:  # CAN THIS BE REMOVED FOR SINGLE SEARCH?

                error_text = "Last in Season"
                controller.open_popup(controller, error_text)

            else:
                self.plant_set_id.set(q_plant_set_id)
                self.saved_plant_set.plant_set_id = self.plant_set_id.get()

                self.saved_plot_id = self.saved_plant_set.plot_id

                self.reset_values(controller)
        except:
            if ValueError:
                print("Value Error")
                pass
            else:
                error_message = "Other error, plant set not found."
                controller.open_popup(controller,
                                      error_message)

    def import_next_plant_set(self, controller):
        try:

            print(self.saved_plant_set.plant_set_id)

            self.current_plant_set = self.saved_plant_set

            self.saved_plant_set = plant_set.PlantSet()

            # begin getting and validating plant selection

            validated_plant = self.validate_plant_selection(controller)
            if validated_plant:
                plant_selection = self.plant_combo.selection
            else:
                raise ValueError

            # end getting and validating plant selection

            # begin getting and validating season selection

            validated_season = self.validate_season_selection(controller)
            if validated_season:
                season_selection = self.season_combo.selection
            else:
                raise ValueError

            # end getting and validating season selection

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

                self.saved_plant_set = self.current_plant_set

            else:
                self.plant_set_id.set(q_plant_set_id)
                self.saved_plant_set.plant_set_id = self.plant_set_id.get()

                self.saved_plot_id = self.saved_plant_set.plot_id

                self.reset_values(controller)

        except:
            if ValueError:
                print("Value Error in Import")
                pass
            else:
                error_message = "Other error, plant set not found."
                controller.open_popup(controller,
                                      error_message)

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
                self.date_planted_entry.set_date(self.saved_plant_set.planted_date)

            self.first_harvest_entry.delete(0, 'end')
            if self.saved_plant_set.first_harvest_date is not None:
                self.first_harvest_entry.set_date(self.saved_plant_set.first_harvest_date)

            self.last_harvest_entry.delete(0, 'end')
            if self.saved_plant_set.last_harvest_date is not None:
                self.last_harvest_entry.set_date(self.saved_plant_set.last_harvest_date)

            print('saved outcome is: ')
            print(self.saved_plant_set.outcome)

            if self.saved_plant_set.outcome is None:
                self.radio_selection = 9
                self.radio1.select()
            elif self.saved_plant_set.outcome == 1:
                self.radio_selection = 1
                self.radio2.select()
            elif self.saved_plant_set.outcome == 0:
                self.radio_selection = 0
                self.radio3.select()

            print('radio selection is')
            print(self.radio_selection)


        except TypeError:
            error_text = "Error resetting values"
            controller.open_popup(controller, error_text)

    def validate_values(self, controller):
        try:
            # begin get and validate plant selection
            validated_plant = self.validate_plant_selection(controller)
            if validated_plant:
                self.plant_id = int(self.plant_combo.get_id(plant_name_query,
                                                            validated_plant))
                print('Plant ID selected is: ' + str(self.plant_id))
            else:
                print('No Plant ID')
                raise ValueError

            # get and validate season selection
            validated_season = self.validate_season_selection(controller)
            if validated_season:
                self.season_id = int(self.season_combo.get_id(seasons_query,
                                                              validated_season))
                print("season ID is " + str(self.season_id))
            else:
                raise ValueError

            # get and validate plot entered
            validated_plot = self.validate_plot_selection(controller)
            if validated_plot:
                self.plot_id = int(validated_plot)
                print('plot is ' + str(self.plot_id))
            else:
                raise ValueError

            # get and validate set quantity entered
            validated_quantity = self.validate_set_quantity_selection(controller)
            if validated_quantity:
                self.set_quantity = int(validated_quantity)
                print('set quantity is ' + str(self.set_quantity))
            else:
                raise ValueError

            # get and validate set type selected
            set_type = self.set_type_combo.selection

            # if a new set type isn't selected, look up type of imported set
            if set_type is None or set_type == '':
                this_connection = data_connection.Connection()  # connect to server
                cursor = this_connection.connection.cursor()  # set connection cursor
                cursor.execute(set_type_query)
                records = cursor.fetchall()
                for r in records:
                    if self.saved_plant_set.set_type == r[1]:
                        self.set_type_id = r[0]

            # otherwise validate the selection made
            else:
                validated_set_type = self.validate_set_type_selection(controller)
                if validated_set_type:
                    print('set type to check is ' + str(set_type))

                    self.set_type_id = int(self.set_type_combo.get_id(set_type_query,
                                                                      validated_set_type))
                    print("Set Type ID is " + str(self.set_type_id))

                else:
                    raise ValueError

            # throw error if the set type ID was not generated by either of the above
            if self.set_type_id is None or set_type == '':
                error_message = ("Missing or invalid Set Type selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            print("Set Type ID is " + str(self.set_type_id))

            # get and validate optional notes entry
            self.set_notes = self.validate_notes_entry(controller)
            print("Set Notes: " + str(self.set_notes))

            # begin getting and validating planted date
            self.planted_date = self.date_planted_entry.get()

            # set date to null if nothing was entered
            if self.planted_date == "":
                print('No planted date entered')
                self.planted_date = None
            else:

                # run the function to validate the date if there is data
                test_planted_date = validate.Validate(self.planted_date)
                planted_date_validation = test_planted_date.validate_date()
                if planted_date_validation:
                    self.planted_date = self.planted_date
                    print('Plant date validation passed')

                    # raise and print error message if it doesn't pass
                elif planted_date_validation is False:
                    error_message = ("Invalid planted date"
                                     "\nPlant set not edited")
                    controller.open_popup(controller,
                                          error_message)
                    self.planted_date = None
                    raise ValueError

                    # do nothing if no data was entered
                else:
                    print('Planted date blank, no error')
                    pass

            # end getting and validating planted date

            # begin getting and validating first harvest date

            self.first_harvest_date = self.first_harvest_entry.get()

            # set date to null if nothing was entered
            if self.first_harvest_date == "":
                print('No harvest date entered')
                self.first_harvest_date = None

            else:
                # run the function to validate the date if there is data
                test_first_harvest_date = validate.Validate(self.first_harvest_date)
                first_harvest_date_validation = test_first_harvest_date.validate_date()
                if first_harvest_date_validation:

                    # check if there is a valid "planted date" entered
                    # raise and print error message if not
                    if self.planted_date is None:
                        error_message = ("Harvest date requires"
                                         "\na valid Planted Date"
                                         "\nPlant set not edited")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

                    # check if the planted date precedes the harvest date
                    # raise and print error message if not
                    elif datetime.strptime(self.planted_date,
                                           '%m/%d/%y') >= datetime.strptime(self.first_harvest_date,
                                                                            '%m/%d/%y'):
                        error_message = ("Harvest date must be at least"
                                         "\none (1) day after date planted."
                                         "\nPlant set not edited.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

                    else:
                        self.first_harvest_date = self.first_harvest_date
                        print('First Harvest date validation passed')

                # raise and print error message if data validation doesn't pass
                elif first_harvest_date_validation is False:
                    error_message = ("Invalid First Harvest date"
                                     "\nPlant set not edited")
                    controller.open_popup(controller,
                                          error_message)
                    self.first_harvest_date = None
                    raise ValueError

                # do nothing if no data was entered
                else:
                    print('First Harvest date blank, no error')
                    pass

            # end getting and validating first harvest date

            # begin getting and validating last harvest date

            self.last_harvest_date = self.last_harvest_entry.get()

            # set date to null if nothing was entered
            if self.last_harvest_date == "":
                print('No last harvest date entered')
                self.last_harvest_date = None
            else:
                # run the function to validate the date if there is data
                test_last_harvest_date = validate.Validate(self.last_harvest_date)
                last_harvest_date_validation = test_last_harvest_date.validate_date()
                if last_harvest_date_validation:

                    # check if there is a valid first harvest date entered
                    # raise and print error message if not
                    if self.first_harvest_date is None:
                        error_message = ("Last Harvest date requires"
                                         "\na valid First Harvest date."
                                         "\nPlant set not edited.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

                    # check if the first harvest date equals or precedes the last harvest date
                    # raise and print error message if not
                    elif datetime.strptime(self.first_harvest_date,
                                           '%m/%d/%y') > datetime.strptime(self.last_harvest_date,
                                                                           '%m/%d/%y'):
                        error_message = ("Last Harvest date must equal"
                                         "\nor follow First Harvest date."
                                         "\nPlant set not edited.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

                    else:

                        self.last_harvest_date = self.last_harvest_date
                        print('last Harvest date validation passed')

                # raise and print error message if data validation doesn't pass
                elif last_harvest_date_validation is False:
                    error_message = ("Invalid Last Harvest date"
                                     "\nPlant set not edited")
                    controller.open_popup(controller,
                                          error_message)
                    self.last_harvest_date = None
                    raise ValueError

                # do nothing if no data was entered
                else:
                    print('Last Harvest date blank, no error')
                    pass
            # end getting and validating last harvest date


            print('radio is: ')
            print(self.radio_selection)


            if self.radio_selection == 9:
                self.outcome = None
            else:
                self.outcome = self.radio_selection

            print('outcome assigned')
            print(self.outcome)

            self.updated_set = plant_set.PlantSet()
            self.updated_set.add_new_plant_set(self.plant_id, self.set_type_id, self.set_quantity)
            print(self.updated_set)


            return True

        except ValueError:
            print("Value Error in edited set1")
            return False
        except Exception:
            error_message = "Other error, plant set not updated."
            controller.open_popup(controller,
                                  error_message)
            return False

    def check_edited_set(self, controller):

        if self.validate_values(controller):
            try:
                print('validation complete, checking plot')

                # check if plot was changed
                self.plot_change = None
                if int(self.plot_id) == int(self.saved_plot_id):
                    self.plot_change = 'N'
                    print('no plot change')
                else:
                    self.plot_change = 'Y'
                    print('plot change')

                print('plot change status captured, checking plan')

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

            except Exception:
                error_message = "Error saving Plant Set."
                controller.open_popup(controller,
                                         error_message)

    def save_unchecked_set(self, controller):

        try:

            self.validate_values(controller)
            self.export_edited_set(controller)


        except:
            if ValueError:
                print("Value Error in edited set")
                pass
            else:
                error_message = "Other error, plant set not updated."
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

        logo_file = "Logo.png"
        logo_folder = "Images"
        path = os.path.abspath(__file__)
        logo_dir = os.path.dirname(path)
        logo_path = os.path.join(logo_dir, logo_folder, logo_file)

        logo = tk.PhotoImage(file=logo_path)
        label = tk.Label(image=logo)
        label.image = logo

        tk.Label(self,
                 image=label.image, border=0).grid(row=5,
                                                   rowspan=3,
                                                   column=4,
                                                   columnspan=3)
        tk.Label(self,
                 text="Garden Setup and Maintenance Menu",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=1,
                                  columnspan=4)
        tk.Label(self,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1,
                                  columnspan=4)
        tk.Button(self,
                  width=15,
                  text="Exit to Main",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(StartPage)).grid(row=3,
                                                                         column=4,
                                                                         sticky='EW')
        tk.Button(self,
                  width=20,
                  text="Add New Zone",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(AddZonesPage)).grid(row=3,
                                                                            column=1,
                                                                            sticky='EW')
        tk.Button(self,
                  width=20,
                  text="Add New Plots",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(AddPlotsPage)).grid(row=3,
                                                                            column=2,
                                                                            sticky='EW')
        tk.Button(self,
                  width=20,
                  text="Add New Season",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(AddSeasonPage)).grid(row=3,
                                                                             column=3,
                                                                             sticky='EW')
        tk.Label(self,
                 text="Brand new? Start by adding New Zones, Plots, then Seasons above.",
                 justify=tk.LEFT,
                 anchor='w',
                 bg='white',
                 fg='dark green',
                 font=MEDIUM_FONT).grid(row=4,
                                        column=1,
                                        columnspan=3)

        tk.Button(self,
                  width=20,
                  text="Edit Individual Plot",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(EditPlotPage)).grid(row=5,
                                                                            column=1,
                                                                            sticky='EW')
        tk.Button(self,
                  width=20,
                  text="Update Plant Set",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(EditSetPage)).grid(row=5,
                                                                           column=2,
                                                                           sticky='EW')
        tk.Button(self,
                  width=20,
                  text="Add New Plant",
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: controller.show_frame(AddPlantPage)).grid(row=5,
                                                                            column=3,
                                                                            sticky='EW')

        for child in self.winfo_children():
            child.grid_configure(padx=10,
                                 pady=10)


# class to add new Zones to the database
# a Zone is a contiguous set of plots
class AddZonesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self,
                 text="Add New Zone",
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
                                        bg='white',
                                        relief='solid')
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
                                        bg='white',
                                        relief='solid')
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
                                           bg='white',
                                           relief='solid')
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
                                       bg='white',
                                       relief='solid')
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

            zone_name = self.zone_name_entry.get()

            # get and validate plant name entry

            zone_name_to_validate = validate.Validate(zone_name)
            if zone_name_to_validate.validate_text():
                self.zone_name = str(zone_name)

            elif zone_name_to_validate.validate_text() is False:
                error_message = ("Invalid Zone Name entered."
                                 "\nAllowed special characters are: -_',:%&()"
                                 "\nNew Zone not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                error_message = ("No Zone Name entered"
                                 "\nNew Zone not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # get and validate row entry

            zone_rows = self.zone_rows_entry.get()

            if zone_rows == "" or zone_rows is None or zone_rows == '0':
                print('No Rows entered')
                error_message = ("Missing Row entry."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # run validation test
            else:
                test_rows = validate.Validate(zone_rows)
                if test_rows.validate_positive_int():
                    print('row validation passed')
                    self.zone_rows = int(zone_rows)
                else:
                    error_message = ("Invalid Row entry."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # get and validate column entry

            zone_columns = self.zone_columns_entry.get()

            if zone_columns == "" or zone_columns is None or zone_columns == '0':
                print('No Columns entered')
                error_message = ("Missing Column entry."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # run validation test
            else:
                test_columns = validate.Validate(zone_columns)
                if test_columns.validate_positive_int():
                    print('column validation passed')
                    self.zone_columns = int(zone_columns)
                else:
                    error_message = ("Invalid Column entry."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            zone_notes = self.zone_notes_text.get(1.0, 'end')

            if zone_notes.strip() == "" or zone_notes.strip() is None:
                self.zone_notes = None

            else:

                test_notes = validate.Validate(zone_notes.strip())
                if test_notes.validate_text():
                    print('notes selection validation passed')
                    self.zone_notes = zone_notes

                else:
                    error_message = ("Invalid Notes entry."
                                     "\nAllowed special characters are: -_',:%&()"
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

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
        except ValueError:
            pass
        except Exception:
            error_message = ("Error saving zone,"
                             "\nZone has not been added.")
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

            # Get and validate zone selection

            zone = self.zone_combo.selection

            if zone == "" or zone is None:
                print('No zone entered')
                error_message = ("Missing Zone selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # Run validation test

            else:
                test_zone = validate.Validate(zone)
                if test_zone.validate_text():
                    print('Zone selection validation passed')
                    self.zone_id = self.zone_combo.get_id(zone_query,
                                                          zone)
                    print(self.zone_id)

                else:
                    error_message = ("Invalid Zone selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            print('zone ID is: ' + str(self.zone_id))

            #  Get and validate row entry

            total_rows = self.quantity_rows_entry.get()

            if (total_rows == ""
                    or total_rows is None
                    or total_rows == '0'):
                print('No Rows entered')
                error_message = ("Missing Row entry."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # run validation test
            else:
                test_rows = validate.Validate(total_rows)
                if test_rows.validate_positive_int():
                    print('row validation passed')
                    self.total_rows = int(total_rows)
                else:
                    error_message = ("Invalid Row entry."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # get and validate column entry

            total_columns = self.quantity_columns_entry.get()

            if (total_columns == ""
                    or total_columns is None
                    or total_columns == '0'):
                print('No Columns entered')
                error_message = ("Missing Column entry."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # run validation test
            else:
                test_columns = validate.Validate(total_columns)
                if test_columns.validate_positive_int():
                    print('column validation passed')
                    self.total_columns = int(total_columns)
                else:
                    error_message = ("Invalid Column entry."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            self.total_plots = self.total_rows * self.total_columns

            # get and validate plot size

            plot_size = self.plot_size_entry.get()

            if (plot_size == ""
                    or plot_size is None
                    or plot_size == '0'):
                print('No Plot Size entered')
                error_message = ("Missing Plot Size entry."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # run validation test
            else:
                test_plot_size = validate.Validate(plot_size)
                if test_plot_size.validate_positive_int():
                    print('plot size validation passed')
                    self.plot_size = int(plot_size)
                else:
                    error_message = ("Invalid Plot Size entry."
                                     "\nPlease enter inches or feet in"
                                     "\nwhole numbers and try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # Get and validate Measurement Unit selection

            measurement_unit_text = self.measurement_combo.selection

            if measurement_unit_text == "" or measurement_unit_text is None:
                print('No Measurement Unit selected')
                error_message = ("Missing Measurement Unit selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # Run validation test

            else:
                test_measurement_unit_text = validate.Validate(measurement_unit_text)
                if test_measurement_unit_text.validate_text():
                    print('Measurement Unit selection validation passed')
                    self.measurement_unit_id = self.measurement_combo.get_id(measurement_unit_query,
                                                                             measurement_unit_text)
                else:
                    error_message = ("Invalid Measurement Unit selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # does not need validation since it's a checkbox
            self.container = bool(self.is_container.get())

            # get and validate container depth if plot is a container
            if self.container:

                container_depth = self.container_depth_entry.get()

                print('container depth')
                print(container_depth)

                if (container_depth == ""
                        or container_depth is None):
                    print('No container_depth entered')
                    error_message = ("Missing Container Depth entry"
                                     "\nand Container is selected."
                                     "\nPlease enter Container Depth.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

                # run validation test
                else:
                    test_container_depth = validate.Validate(container_depth)
                    if test_container_depth.validate_positive_float():
                        print('container_depth validation passed')
                        self.container_depth = float(container_depth)
                        self.container_depth  = round(self.container_depth, 2)
                    else:
                        error_message = ("Invalid Container Depth entry."
                                         "\nPlease enter inches in"
                                         "\nwhole numbers and try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

            # Get and validate Sun Level selection

            sun_text = self.sun_combo.selection

            if sun_text == "" or sun_text is None:
                print('No Sun Level selected')
                error_message = ("Missing Sun Level selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # Run validation test
            else:
                test_sun_text = validate.Validate(sun_text)
                if test_sun_text.validate_text():
                    print('sun selection validation passed')
                    self.sun_id = self.measurement_combo.get_id(sun_query,
                                                                sun_text)

                else:
                    error_message = ("Invalid Sun Level selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # Get and validate Soil Moisture selection

            soil_moisture_text = self.soil_moisture_combo.selection

            if soil_moisture_text == "" or soil_moisture_text is None:
                print('No soil_moisture_text Level selected')
                error_message = ("Missing Soil Moisture Level selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # Run validation test

            else:
                test_soil_moisture_text = validate.Validate(soil_moisture_text)
                if test_soil_moisture_text.validate_text():
                    print('soil_moisture selection validation passed')
                    self.soil_moisture_id = self.measurement_combo.get_id(soil_moisture_query,
                                                                          soil_moisture_text)
                else:
                    error_message = ("Invalid Soil Moisture Level selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            this_connection = data_connection.Connection()  # connect to server
            cursor = this_connection.connection.cursor()  # set connection cursor

            print('Connected')
            print(self.zone_id)

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

            print('empty plot list created')

            for id in range(self.total_plots):
                self.new_plot = plot.Plot()

                if column > self.total_columns:
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

            #  display confirmation popup
            success_message = (str(self.total_plots) + ' Plots added successfully!')
            controller.open_popup(controller,
                                  success_message)

        # error handling for missing or invalid data
        except ValueError:
            pass
        except Exception:
            error_message = "Error saving new plots" \
                            "\nplots not added."
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
            self.set_plot_spinbox()

        except:
            error_message = "Error connecting to database"
            controller.open_popup(controller,
                                  error_message)


    # sets default label and data values for new window

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

    def set_plot_spinbox(self):
        # setup spinbox with the highest plot ID number as max value
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

        # create object to store imported plot data
        self.saved_plot = plot.Plot()

        # get plot ID to search from entry screen
        plot_id = self.plot_spinbox.get()

        # attempt to import the entered plot
        self.plot_id = self.saved_plot.import_plot(plot_id)

        # error if plot is not found
        if self.plot_id is None:
            error_text = "Plot Not Found"
            controller.open_popup(controller, error_text)
        else:
            print(self.plot_id)

        # if the plot is found in the database
        # run function to reset values to imported plot data
        if self.plot_id is not None:
            self.reset_values()
        else:
        # otherwise reset screen to defaults
            self.set_default_values(controller)

    # Function to reset interface widgets with imported values
    def reset_values(self):

        # delete or deselect current entries
        # and replace with imported values

        self.plot_active_checkbox.deselect()
        if self.saved_plot.plot_active is True:
            self.plot_active_checkbox.select()
        else:
            self.plot_active_checkbox.deselect()

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

        self.is_container_checkbox.deselect()
        self.container_depth_entry.delete(0, 'end')

        if self.saved_plot.is_container is True:
            self.is_container_checkbox.select()
            self.container_depth_entry.insert(0, self.saved_plot.container_depth)
        else:
            self.is_container_checkbox.deselect()

    # Function to run standard and custom validation checks
    def validate_edited_plot(self, controller):

        try:

            # make sure plot was selected, error if not
            if (self.plot_id == ""
                    or self.plot_id is None
                    or self.plot_id == 0):
                error_text = ("No plot selected to edit.\n"
                            "Please select a plot and try again.")
                controller.open_popup(controller, error_text)
                self.set_default_values(controller)
                raise ValueError
            else:
                print(self.plot_id)

            # get and validate plot size
            plot_size = self.plot_size_entry.get()
            if (plot_size == ""
                    or plot_size is None
                    or plot_size == '0'):
                print('No Plot Size entered')
                error_message = ("Missing Plot Size entry."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                test_plot_size = validate.Validate(plot_size)
                if test_plot_size.validate_positive_int():
                    print('plot size validation passed')
                    self.plot_size = int(plot_size)
                else:
                    error_message = ("Invalid Plot Size entry."
                                     "\nPlease enter inches or feet in"
                                     "\nwhole numbers and try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # Get and validate Measurement Unit selection
            measurement_unit_text = self.measurement_combo.combo.get()
            if measurement_unit_text == "" or measurement_unit_text is None:
                print('No Measurement Unit selected')
                error_message = ("Missing Measurement Unit selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                test_measurement_unit_text = validate.Validate(measurement_unit_text)
                if test_measurement_unit_text.validate_text():
                    print('Measurement Unit selection validation passed')
                    self.measurement_unit_id = self.measurement_combo.get_id(measurement_unit_query,
                                                                             measurement_unit_text)
                else:
                    error_message = ("Invalid Measurement Unit selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # Get container status selection
            # No validation required for checkbox
            if self.is_container.get() == 1:
                self.container = bool(True)
            else:
                self.container = bool(False)
                self.container_depth = None

            # get and validate container depth if plot is a container
            if self.container:
                container_depth = self.container_depth_entry.get()
                if (container_depth == ""
                        or container_depth is None):
                    print('No container_depth entered')
                    error_message = ("Missing Container Depth entry"
                                     "\nand Container is selected."
                                     "\nPlease enter Container Depth.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError
                else:
                    test_container_depth = validate.Validate(container_depth)
                    if test_container_depth.validate_positive_float():
                        print('container_depth validation passed')
                        self.container_depth = float(container_depth)
                        self.container_depth  = round(self.container_depth, 2)
                    else:
                        error_message = ("Invalid Container Depth entry."
                                         "\nPlease enter inches in"
                                         "\nwhole numbers and try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError

            # Get and validate nitrogen level
            nitrogen_level = self.nitrogen_level_entry.get()
            if (nitrogen_level == ""
                    or nitrogen_level is None
                    or nitrogen_level == '0'):
                print('No Nitrogen Level entered')
                error_message = ("Missing Nitrogen Level entry."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                test_nitrogen_level = validate.Validate(nitrogen_level)
                if test_nitrogen_level.validate_int():
                    print('nitrogen_level validation passed')
                    self.nitrogen_level = int(nitrogen_level)
                else:
                    error_message = ("Invalid Nitrogen Level entry."
                                     "\nWhole numbers only."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # Get and validate Sun Level selection
            sun_text = self.sun_combo.combo.get()
            if sun_text == "" or sun_text is None:
                print('No Sun Level selected')
                error_message = ("Missing Sun Level selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                test_sun_text = validate.Validate(sun_text)
                if test_sun_text.validate_text():
                    print('sun selection validation passed')
                    self.sun_id = self.measurement_combo.get_id(sun_query,
                                                                sun_text)
                else:
                    error_message = ("Invalid Sun Level selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # Get and validate Soil Moisture selection
            soil_moisture_text = self.soil_moisture_combo.combo.get()
            if soil_moisture_text == "" or soil_moisture_text is None:
                print('No soil_moisture_text Level selected')
                error_message = ("Missing Soil Moisture Level selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError
            else:
                test_soil_moisture_text = validate.Validate(soil_moisture_text)
                if test_soil_moisture_text.validate_text():
                    print('soil_moisture selection validation passed')
                    self.soil_moisture_id = self.measurement_combo.get_id(soil_moisture_query,
                                                                          soil_moisture_text)
                else:
                    error_message = ("Invalid Soil Moisture Level selection."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            # Get plot active status
            # No validation required for checkbox
            if self.plot_active.get() == 1:
                self.is_active = bool(True)
            else:
                self.is_active = bool(False)

            return True

        except ValueError:
            return False

        except Exception:
            error_message = "Other error, plot not updated."
            controller.open_popup(controller,
                                  error_message)
            return False

    def export_edited_plot(self, controller):

        if self.validate_edited_plot(controller):
            try:
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

                #  display confirmation popup
                success_message = ('Plot ' + str(self.plot_id) + ' updated successfully!')
                controller.open_popup(controller,
                                      success_message)

            except Exception:
                error_message = "Error saving plot."
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

            if self.radio_selection == 1:
                self.season = "Spring"
            if self.radio_selection == 2:
                self.season = "Fall"

            # error if neither season was checked
            if not self.radio_selection == 1 and not self.radio_selection == 2:
                error_message = ("Missing Spring or Fall selection"
                                 "\nNew plant not added.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # get and validate year entry

            year = self.year_spinbox.get()

            if year == "" or year is None or year == '0':
                print('No year entered')
                error_message = ("Missing year selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # run validation test
            else:
                test_year = validate.Validate(year)
                if test_year.validate_positive_int():
                    if 2000 <= int(year) <= 3000:
                        print('year validation passed')
                        self.year = year

                    else:
                        error_message = ("Invalid Year entry."
                                         "\nPlease try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError
                else:
                    error_message = ("Invalid Year entry."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

            new_season = my_season.MySeason()
            new_season.set_season_values(self.season, self.year)
            new_season_text = new_season.export_season()

            # display confirmation popup
            success_message = ("Season generated successfully:\n"
                               + new_season_text)
            controller.open_popup(controller,
                                  success_message)

            # error handling for missing or invalid data
        except ValueError:
            pass
        except Exception:
            error_message = "Missing or invalid data, season not added."
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
        logo_folder = "Images"
        path = os.path.abspath(__file__)
        logo_dir = os.path.dirname(path)
        logo_path = os.path.join(logo_dir, logo_folder, logo_file)

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
                  command=lambda: PlantingPlanReport(controller)).grid(row=4,
                                                                       column=2,
                                                                       sticky='W')
        tk.Button(self,
                  width=30,
                  text="All Plants Detail",
                  bg='dark green',
                  fg='white',
                  command=lambda: PlantsDetailReport(controller)
                  ).grid(row=4, column=3, sticky='E')

        tk.Button(self,
                  width=30,
                  text="Outcome Summary",
                  bg='dark green',
                  fg='white',
                  command=lambda: OutcomeSummaryReport(controller)).grid(row=5,
                                                                         column=2,
                                                                         sticky='E')
        tk.Button(self,
                  width=30,
                  text="Outcome Detail",
                  bg='dark green',
                  fg='white',
                  command=lambda: OutcomeDetailReport(controller)).grid(row=5,
                                                                        column=3,
                                                                        sticky='E')
        for child in self.winfo_children():
            child.grid_configure(padx=10,
                                 pady=10)


class PlantingPlanReport(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)

        # set formatting for just this window
        top = tk.Toplevel(self)
        top.configure(bg='white',
                      padx=25,
                      pady=25)

        # set title for just this window
        top.title("Planting Plan report")

        # icon in the top left corner
        icon_file = "Icon.png"

        # icon in the top left corner
        icon_file = "Icon.png"
        icon_folder = "Images"

        # set file path for logo file location
        path = os.path.abspath(__file__)
        icon_dir = os.path.dirname(path)
        icon_path = os.path.join(icon_dir, icon_folder, icon_file)

        img = tk.PhotoImage(file=icon_path)
        top.iconphoto(False, img)

        self.set_labels(controller, top)

    def set_labels(self, controller, top):

        tk.Label(top,
                 text="My Planting Plan Report",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(top,
                  width=15,
                  text="Close Report Window",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: top.destroy()).grid(row=2,
                                                      column=8,
                                                      sticky='EW')
        tk.Label(top,
                 text='Click "Refresh" to reflect changes: ',
                 anchor='e',
                 justify=tk.RIGHT,
                 font=MEDIUM_FONT,
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)
        tk.Button(top,
                  width=10,
                  text="Refresh",
                  anchor='center',
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.refresh_planting_plan(controller,
                                                             top)).grid(row=3,
                                                                        column=3)
        tk.Button(top,
                  width=15,
                  text="Export (save) to CSV",
                  anchor='w',
                  justify=tk.LEFT,
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_planting_plan(controller, top)).grid(row=3,
                                                                              column=5)
        tk.Label(top,
                 text="Hint: Export to view all data if list exceeds screen size.",
                 bg='white').grid(row=3,
                                  column=6,
                                  columnspan=4)
        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)

        tk.Label(top,
                 text="Plant",
                 bg='white').grid(row=5,
                                  column=1)

        tk.Label(top,
                 text="Season",
                 bg='white').grid(row=5,
                                  column=2)

        tk.Label(top,
                 text="Zone",
                 bg='white').grid(row=5,
                                  column=3)

        tk.Label(top,
                 text="Plot",
                 bg='white').grid(row=5,
                                  column=4)

        tk.Label(top,
                 text=" Space / Seed Pack ",
                 bg='white').grid(row=5,
                                  column=5)

        tk.Label(top,
                 text=" Space / Seedling ",
                 bg='white').grid(row=5,
                                  column=6)

        tk.Label(top,
                 text=" Depth for Seeds ",
                 bg='white').grid(row=5,
                                  column=7)

        tk.Label(top,
                 text=" Watering Frequency ",
                 bg='white').grid(row=5,
                                  column=8)

        tk.Label(top,
                 text=" Days to Harvest ",
                 bg='white').grid(row=5,
                                  column=9)

        self.query_plan(controller, top)

    def reset_grid(self, top):
        for label in top.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def refresh_planting_plan(self, controller, top):
        self.reset_grid(top)
        self.set_labels(controller, top)
        self.query_plan(controller, top)

    def query_plan(self, controller, top):
        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(planting_plan_query)

            for row_number, row in enumerate(cursor, 6):
                tk.Label(top,
                         text=str(row[1]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[2]),
                         bg='white').grid(column=2,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[3]),
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[4]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[5]) + ' inches',
                         bg='white').grid(column=5,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[6]) + ' inches',
                         bg='white').grid(column=6,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[7]) + ' inches',
                         bg='white').grid(column=7,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[8]),
                         bg='white').grid(column=8,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[9]),
                         bg='white').grid(column=9,
                                          row=row_number)

            this_connection.end_connection()

        except:
            error_message = "Error displaying Planting Plan Report"
            controller.open_popup(controller,
                                  error_message)

    def export_planting_plan(self, controller, top):

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

            success_message = "File Saved: \n" + download_path
            controller.open_popup(controller,
                                  success_message)

        except:
            error_message = "Error exporting Planting Plan Report"
            controller.open_popup(controller,
                                  error_message)


class PlantsDetailReport(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)

        # set formatting for just this window
        top = tk.Toplevel(self)
        top.configure(bg='white',
                      padx=25,
                      pady=25)

        # set title for just this window
        top.title("All Plant Details report")

        # icon in the top left corner
        icon_file = "Icon.png"
        icon_folder = "Images"
        # set file path for logo file location
        path = os.path.abspath(__file__)
        icon_dir = os.path.dirname(path)
        icon_path = os.path.join(icon_dir, icon_folder, icon_file)

        img = tk.PhotoImage(file=icon_path)
        top.iconphoto(False, img)

        self.set_labels(controller, top)

    def set_labels(self, controller, top):
        tk.Label(top,
                 text="All Plants Detail Report",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(top,
                  width=15,
                  text="Close Report Window",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: top.destroy()).grid(row=2,
                                                      column=8,
                                                      sticky='EW')

        tk.Label(top,
                 text='Click "Refresh" to reflect changes: ',
                 anchor='e',
                 justify=tk.RIGHT,
                 font=MEDIUM_FONT,
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        tk.Button(top,
                  width=10,
                  text="Refresh",
                  anchor='center',
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.refresh_all_plants(controller, top)).grid(row=3,
                                                                                 column=3)

        tk.Button(top,
                  width=15,
                  text="Export (save) to CSV",
                  anchor='w',
                  justify=tk.LEFT,
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_all_plants(controller)).grid(row=3,
                                                                           column=5)
        tk.Label(top,
                 text="Hint: Export to view all data if list exceeds screen size.",
                 bg='white').grid(row=3,
                                  column=6,
                                  columnspan=4)
        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)
        tk.Label(top,
                 text="Plant",
                 bg='white').grid(row=5,
                                  column=1)
        tk.Label(top,
                 text="In Plan?",
                 bg='white').grid(row=5,
                                  column=2)
        tk.Label(top,
                 text=" Crop Group ",
                 bg='white').grid(row=5,
                                  column=3)
        tk.Label(top,
                 text=" Sun Required ",
                 bg='white').grid(row=5,
                                  column=4)
        tk.Label(top,
                 text=" Soil Moisture ",
                 bg='white').grid(row=5,
                                  column=5)
        tk.Label(top,
                 text=" Space / Seed Pack ",
                 bg='white').grid(row=5,
                                  column=6)
        tk.Label(top,
                 text=" Space / Seedling ",
                 bg='white').grid(row=5,
                                  column=7)
        tk.Label(top,
                 text=" Depth Requirement ",
                 bg='white').grid(row=5,
                                  column=8)
        tk.Label(top,
                 text=" Watering Frequency ",
                 bg='white').grid(row=5,
                                  column=9)
        tk.Label(top,
                 text=" Frost Tolerance ",
                 bg='white').grid(row=5,
                                  column=10)
        tk.Label(top,
                 text=" Days to Harvest ",
                 bg='white').grid(row=5,
                                  column=11)
        tk.Label(top,
                 text="Plant in Spring?",
                 bg='white').grid(row=5,
                                  column=12)
        tk.Label(top,
                 text="Plant in Fall?",
                 bg='white').grid(row=5,
                                  column=13)
        self.query_all_plants(controller, top)

    def reset_grid(self, top):
        for label in top.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def refresh_all_plants(self, controller, top):
        self.reset_grid(top)
        self.set_labels(controller, top)
        self.query_all_plants(controller, top)

    def query_all_plants(self, controller, top):

        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(plant_detail_query)

            for row_number, row in enumerate(cursor, 6):
                tk.Label(top,
                         text=str(row[1]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[2]),
                         bg='white').grid(column=2,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[3]),
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[4]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[5]),
                         bg='white').grid(column=5,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[6]) + ' inches',
                         bg='white').grid(column=6,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[7]) + ' inches',
                         bg='white').grid(column=7,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[8]) + ' inches',
                         bg='white').grid(column=8,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[9]),
                         bg='white').grid(column=9,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[10]),
                         bg='white').grid(column=10,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[11]) + ' days',
                         bg='white').grid(column=11,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[12]),
                         bg='white').grid(column=12,
                                          row=row_number)
                tk.Label(top,
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

            success_message = "File Saved: \n" + download_path
            controller.open_popup(controller,
                                  success_message)

        except:
            error_message = "Error exporting Plant Detail Report"
            controller.open_popup(controller,
                                  error_message)


class OutcomeDetailReport(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)

        # set formatting for just this window
        top = tk.Toplevel(self)
        top.configure(bg='white',
                      padx=25,
                      pady=25)

        # set title for just this window
        top.title("Outcome Detail report")

        # icon in the top left corner
        icon_file = "Icon.png"
        icon_folder = "Images"
        # set file path for logo file location
        path = os.path.abspath(__file__)
        icon_dir = os.path.dirname(path)
        icon_path = os.path.join(icon_dir, icon_folder, icon_file)

        img = tk.PhotoImage(file=icon_path)
        top.iconphoto(False, img)

        self.set_labels(controller, top)

    def set_labels(self, controller, top):

        tk.Label(top,
                 text="Outcome Detail Report",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(top,
                  width=15,
                  text="Close Report Window",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: top.destroy()).grid(row=2,
                                                      column=8,
                                                      sticky='EW')

        tk.Label(top,
                 text='Click "Refresh" to reflect changes: ',
                 anchor='e',
                 justify=tk.RIGHT,
                 font=MEDIUM_FONT,
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        tk.Button(top,
                  width=10,
                  text="Refresh",
                  anchor='center',
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.refresh_outcome_detail(controller, top)).grid(row=3,
                                                                                     column=3)

        tk.Button(top,
                  width=15,
                  text="Export (save) to CSV",
                  anchor='w',
                  justify=tk.LEFT,
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_outcome_detail(controller)).grid(row=3,
                                                                               column=5)

        tk.Label(top,
                 text="Hint: Export to view all data if list exceeds screen size.",
                 bg='white').grid(row=3,
                                  column=6,
                                  columnspan=4)
        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)
        tk.Label(top,
                 text="Plant Set ID",
                 bg='white').grid(row=5,
                                  column=1)
        tk.Label(top,
                 text="Season",
                 bg='white').grid(row=5,
                                  column=2)
        tk.Label(top,
                 text="Plant",
                 bg='white').grid(row=5,
                                  column=3)
        tk.Label(top,
                 text="Zone",
                 bg='white').grid(row=5,
                                  column=4)
        tk.Label(top,
                 text="Plot",
                 bg='white').grid(row=5,
                                  column=5)
        tk.Label(top,
                 text=" Set Quantity ",
                 bg='white').grid(row=5,
                                  column=6)
        tk.Label(top,
                 text=" Set Type ",
                 bg='white').grid(row=5,
                                  column=7)
        tk.Label(top,
                 text=" Date Planted ",
                 bg='white').grid(row=5,
                                  column=8)
        tk.Label(top,
                 text=" First Harvest ",
                 bg='white').grid(row=5,
                                  column=9)
        tk.Label(top,
                 text=" Last Harvest ",
                 bg='white').grid(row=5,
                                  column=10)
        tk.Label(top,
                 text="Outcome",
                 bg='white').grid(row=5,
                                  column=11)

        self.query_outcome_detail(controller, top)

    def reset_grid(self, top):
        for label in top.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def refresh_outcome_detail(self, controller, top):
        self.reset_grid(top)
        self.set_labels(controller, top)
        self.query_outcome_detail(controller, top)

    def query_outcome_detail(self, controller, top):

        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(outcome_detail_query)

            for row_number, row in enumerate(cursor, 6):
                tk.Label(top,
                         text=str(row[0]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[1]),
                         bg='white').grid(column=2,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[2]),
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[3]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[4]),
                         bg='white').grid(column=5,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[5]),
                         bg='white').grid(column=6,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[6]),
                         bg='white').grid(column=7,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[7]),
                         bg='white').grid(column=8,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[8]),
                         bg='white').grid(column=9,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[9]),
                         bg='white').grid(column=10,
                                          row=row_number)
                tk.Label(top,
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

            success_message = "File Saved: \n" + download_path
            controller.open_popup(controller,
                                  success_message)
        except:
            error_message = "Error exporting Outcome Detail Report"
            controller.open_popup(controller,
                                  error_message)


class OutcomeSummaryReport(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)

        # set formatting for just this window
        top = tk.Toplevel(self)
        top.configure(bg='white',
                      padx=25,
                      pady=25)

        # set title for just this window
        top.title("Outcome Summary report")

        # icon in the top left corner
        icon_file = "Icon.png"
        icon_folder = "Images"
        # set file path for logo file location
        path = os.path.abspath(__file__)
        icon_dir = os.path.dirname(path)
        icon_path = os.path.join(icon_dir, icon_folder, icon_file)

        img = tk.PhotoImage(file=icon_path)
        top.iconphoto(False, img)

        self.set_labels(controller, top)

    def set_labels(self, controller, top):

        tk.Label(top,
                 text="Outcome Summary Report",
                 font=LARGE_FONT,
                 fg='dark green',
                 bg='white').grid(row=1,
                                  column=2,
                                  columnspan=4)
        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=2,
                                  column=1)
        tk.Button(top,
                  width=15,
                  text="Close Report Window",
                  bg='dark red',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: top.destroy()).grid(row=2,
                                                      column=8,
                                                      sticky='EW')
        tk.Label(top,
                 text='Click "Refresh" to reflect changes: ',
                 anchor='e',
                 justify=tk.RIGHT,
                 font=MEDIUM_FONT,
                 bg='white').grid(row=3,
                                  column=1,
                                  columnspan=2)

        tk.Button(top,
                  width=10,
                  text="Refresh",
                  anchor='center',
                  justify=tk.CENTER,
                  bg='white',
                  fg='dark green',
                  font='Helvetica 10',
                  command=lambda: self.refresh_outcome_summary(controller, top)).grid(row=3,
                                                                                      column=3)

        tk.Button(top,
                  width=15,
                  text="Export (save) to CSV",
                  anchor='w',
                  justify=tk.LEFT,
                  bg='dark green',
                  fg='white',
                  font='Helvetica 10',
                  command=lambda: self.export_outcome_summary(controller)).grid(row=3,
                                                                                column=5)

        tk.Label(top,
                 text="Hint: Export to view all data if list exceeds screen size.",
                 bg='white').grid(row=3,
                                  column=6,
                                  columnspan=4)

        tk.Label(top,
                 text=" ",
                 bg='white').grid(row=4,
                                  column=1)

        tk.Label(top,
                 text="Plant Name",
                 bg='white').grid(row=5,
                                  column=1)

        tk.Label(top,
                 text=" Times Planted ",
                 bg='white').grid(row=5,
                                  column=2)

        tk.Label(top,
                 text=" Success Ratio ",
                 bg='white').grid(row=5,
                                  column=3)

        tk.Label(top,
                 text=" Most Recent Season ",
                 bg='white').grid(row=5,
                                  column=4)

        tk.Label(top,
                 text=" Most Recent Outcome ",
                 bg='white').grid(row=5,
                                  column=5)

        self.query_outcome_summary(controller, top)

    def reset_grid(self, top):
        for label in top.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def refresh_outcome_summary(self, controller, top):
        self.reset_grid(top)
        self.set_labels(controller, top)
        self.query_outcome_summary(controller, top)

    def query_outcome_summary(self, controller, top):

        try:
            this_connection = data_connection.Connection()
            cursor = this_connection.connection.cursor()

            cursor.execute(outcome_summary_query)

            for row_number, row in enumerate(cursor, 6):
                tk.Label(top,
                         text=str(row[0]),
                         bg='white').grid(column=1,
                                          row=row_number)
                tk.Label(top,
                         text=str(round(row[1])),
                         bg='white').grid(column=2,
                                          row=row_number)
                if row[2] is None:
                    ratio_text = 'N/A'
                else:
                    ratio_text = str(round(row[2], 2)) + '%'

                tk.Label(top,
                         text=ratio_text,
                         bg='white').grid(column=3,
                                          row=row_number)
                tk.Label(top,
                         text=str(row[3]),
                         bg='white').grid(column=4,
                                          row=row_number)
                tk.Label(top,
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

            success_message = "File Saved: \n" + download_path
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

    def reset_grid(self):
        for label in self.winfo_children():
            if type(label) == tk.Label:
                label.destroy()

    def import_values(self, controller):
        try:
            self.reset_grid()
            self.set_default_values()

            self.closeout_year = planting_year.PlantingYear()

            # get and validate year entry

            year = self.year_spinbox.get()

            if year == "" or year is None or year == '0':
                print('No year entered')
                error_message = ("Missing year selection."
                                 "\nPlease try again.")
                controller.open_popup(controller,
                                      error_message)
                raise ValueError

            # run validation test
            else:
                test_year = validate.Validate(year)
                if test_year.validate_positive_int():
                    if int(year) >= 2000 and int(year) <= 3000:
                        print('year validation passed')
                        self.closeout_year.my_year = int(year)

                    else:
                        error_message = ("Invalid Year entry."
                                         "\nPlease try again.")
                        controller.open_popup(controller,
                                              error_message)
                        raise ValueError
                else:
                    error_message = ("Invalid Year entry."
                                     "\nPlease try again.")
                    controller.open_popup(controller,
                                          error_message)
                    raise ValueError

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

        except ValueError:
            pass
        except Exception:
            error_message = ("Year not found in database."
                             "\nPlease make a new selection.")
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
