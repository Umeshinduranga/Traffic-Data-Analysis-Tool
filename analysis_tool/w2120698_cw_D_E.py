# Task D: Histogram Display 
import tkinter as tk
from collections import defaultdict
import csv
# import task abc as a module 
# and error handling if module not found
try:
    from functions import process_csv_data,validate_continue_input
except ImportError as e:
    print("Error importing module. check the module is available and correctly named.")
    raise e

# define histrigram calss with variaous functions

class HistogramApp:
    def __init__(self, traffic_data, selected_date):

        """
        Initializes the histogram application with the traffic data and selected date.

        Parameters:
            traffic_data: a dictionay of traffic counts per hour and junction
            selected_date: the date selected for the histogram
        """

        # this dict store data for elm 
        self.traffic_data_elm = {} 
        # this is also store data for hanley
        self.traffic_data_hanley = {}
        # Process the traffic data by junction
        self.process_junction_data(traffic_data)
        self.selected_date = selected_date
        # width of gui window 
        self.win_width = 1200
        # height of gui window
        self.win_height = 650
        # width of bar
        self.bar_width = 17
        # max value of traffic data
        self.max_value = max(
            max(self.traffic_data_elm.values() or [0]),
            max(self.traffic_data_hanley.values() or [0])
        )
        # margin of gui window
        self.margin = 75
        # colors for gui window,bar,grid and txet
        self.colors = {
            'elm': {'fill': '#95fb97', 'outline': '#646b6a'}, # collor and outline for elm 
            'hanley': {'fill': '#fd9596', 'outline': '#646b6a'}, # collor and outline for hanley
            'background': '#edf2ee', # background dark white color 
            'grid': '#E0E0E0', # grid color
            'text': '#333333', # text is gray color
        }


    # split data by juctions and hours 
    def process_junction_data(self, traffic_data):

        """
        get traffice data hours by elm and hanley junctions
        """

        # loop through 24 hours 
        for hour in range(24):
            # convert hour to string 
            hour_str = f"{hour:02d}"
            # store trafic data and , default to 0 if not found
            self.traffic_data_elm[hour_str] = traffic_data.get((hour_str, "Elm Avenue/Rabbit Road"), 0)
            self.traffic_data_hanley[hour_str] = traffic_data.get((hour_str, "Hanley Highway/Westway"), 0)


    # create a tkinter window
    def setup_window(self):

        """
        Sets up the Tkinter window and canvas for the histogram.
        """

        # create a main window
        root = tk.Tk()
        root.title("Histogram ") # window title 
        root.geometry(f"{self.win_width}x{self.win_height}") # window size
        # create a canvas
        canvas = tk.Canvas(root, width=self.win_width, height=self.win_height, 
                         bg=self.colors['background'])
        canvas.pack(expand=True, fill='both', padx=10, pady=10)
        # return root and canvas
        return root, canvas


    # draw grid for better read values
    def draw_grid(self, canvas):

        """
        Draw grid lines for better readability.
        """
        # width in to 24 equal sections  (for grid)
        x_interval = (self.win_width - 2 * self.margin) / 24
        for i in range(24):
            # draw vertical lines
            x = self.margin + i * x_interval
            canvas.create_line(x, self.margin, x, 
                             self.win_height - self.margin,
                             fill=self.colors['grid'], dash=(2, 4))

        # height in to 10 equal sections
        y_interval = (self.win_height - 2 * self.margin) / 10
        for i in range(1, 11):
            # draw horizontal lines
            y = self.win_height - self.margin - (i * y_interval)
            canvas.create_line(self.margin, y,
                             self.win_width - self.margin, y,
                             fill=self.colors['grid'], dash=(2, 4))

    # draw axes  x and y 
    def draw_axes(self, canvas):

        """
        Draw the x axes and labels.
        """
        # call grid function to draw grid
        self.draw_grid(canvas)
        canvas.create_line(self.margin, self.win_height - self.margin,
                  self.win_width - self.margin, self.win_height - self.margin,
                  fill=self.colors['text'], width=1, smooth=True)
        # draw x 
        x_interval = (self.win_width - 2 * self.margin) / 24
        for i in range(24):
            x = self.margin + i * x_interval
            canvas.create_text(x + x_interval/2, self.win_height - self.margin + 20,
                             text=f"{i:02d}", anchor='n',
                             font=('Arial', 9), fill=self.colors['text'])

    # this functions is used to draw histogram
    def draw_histogram(self, canvas):

        """
        Draw the histogram bars.
        """
        # width in to 24 equal sections
        x_interval = (self.win_width - 2 * self.margin) / 24
        y_scale = (self.win_height - 2 * self.margin) / self.max_value if self.max_value > 0 else 1

        for hour in range(24):
            hour_str = f"{hour:02d}"
            
            # Elm Road bar
            # get data for elm for this hour
            elm_volume = self.traffic_data_elm.get(hour_str, 0)
            # calculate bar hight 
            elm_height = elm_volume * y_scale
            # left side of bar
            x1_elm = self.margin + hour * x_interval + 8
            # top side of bar
            y1_elm = self.win_height - self.margin - elm_height
            # right side of bar
            x2_elm = x1_elm + self.bar_width
            # bottom side of bar
            y2_elm = self.win_height - self.margin
            

            # add text for volume of each bar
            if elm_volume > 0:
                canvas.create_text((x1_elm + x2_elm) / 2, y1_elm - 5,
                                 text=str(elm_volume), anchor='s',
                                 font=('Arial', 8,'bold'), fill=self.colors['elm']['outline'])
            # draw bar for elm(green)
            canvas.create_rectangle(x1_elm, y1_elm, x2_elm, y2_elm,
                                 fill=self.colors['elm']['fill'],
                                 outline=self.colors['elm']['outline'])
            
            
            # Hanley Highway bar
            # get data for hanley from this hour
            hanley_volume = self.traffic_data_hanley.get(hour_str, 0)
            # calculate bar hight on count 
            hanley_height = hanley_volume * y_scale
            # left side of bar ( next elm bar)
            x1_hanley = x2_elm + 2
            # top of the bar
            y1_hanley = self.win_height - self.margin - hanley_height
            # right side of bar 
            x2_hanley = x1_hanley + self.bar_width
            # bottom of the bar
            y2_hanley = self.win_height - self.margin
            
            # add text for volume of each bar
            if hanley_volume > 0:
                canvas.create_text((x1_hanley + x2_hanley) / 2, y1_hanley - 5,
                                 text=str(hanley_volume), anchor='s',
                                 font=('Arial', 8,'bold'), fill=self.colors['hanley']['outline'])
            # draw bar for hanley(red)
            canvas.create_rectangle(x1_hanley, y1_hanley, x2_hanley, y2_hanley,
                                 fill=self.colors['hanley']['fill'],
                                 outline=self.colors['hanley']['outline'])

        # add title and lables 
        title = f"Histogram of Vehicle Frequency per Hour ({self.selected_date})"
        canvas.create_text(self.win_width/2, 25,
                         text=title,
                         font=('Arial', 16, 'bold'),
                         fill=self.colors['text'])
        # add legend
        self.add_legend(canvas)

        # add x lable
        canvas.create_text(self.win_width/2, self.win_height - 22,
                         text="Hours 00:00 to 24:00",
                         font=('Arial', 10,),
                         fill=self.colors['text'],
                         anchor='s')
        # add y lable
        canvas.create_text(25, self.win_height/2,
                         text="Number of Vehicles",
                         font=('Arial', 10),
                         fill=self.colors['text'],
                         angle=90)

    # this function is used to add legend to the histogram
    def add_legend(self, canvas):

        """
        Adds a legend to the histogram.
        """
        # legend box width and height
        legend_box_width = 20
        legend_box_height = 15
        legend_x = self.margin
        legend_y = 60
        
        # draw legend box for elm 
        canvas.create_rectangle(legend_x, legend_y,
                              legend_x + legend_box_width,
                              legend_y + legend_box_height,
                              fill=self.colors['elm']['fill'],
                              outline=self.colors['elm']['outline'])
        # add text for elm
        canvas.create_text(legend_x + legend_box_width + 5,
                          legend_y + legend_box_height/2,
                          text="Elm Avenue/Rabbit Road",
                          anchor='w',
                          font=('Arial', 10),
                          fill=self.colors['text'])
        
        # draw legend box for hanley
        canvas.create_rectangle(legend_x,
                              legend_y + legend_box_height + 5,
                              legend_x + legend_box_width,
                              legend_y + 2 * legend_box_height + 5,
                              fill=self.colors['hanley']['fill'],
                              outline=self.colors['hanley']['outline'])
        # add text for hanley
        canvas.create_text(legend_x + legend_box_width + 5,
                          legend_y + 1.5 * legend_box_height + 5,
                          text="Hanley Highway/Westway",
                          anchor='w',
                          font=('Arial', 10),
                          fill=self.colors['text'])

    def run(self):

        """
        Runs the Tkinter main loop to display the histogram.
        """
        # call setup window function to create window and canvas
        root, canvas = self.setup_window()
        self.draw_axes(canvas)
        self.draw_histogram(canvas)
        root.mainloop() # run main loop

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):

        """
        Initializes the application for processing multiple CSV files.
        """
        # hold currnt data set and outcomes 
        self.current_data = None
        self.outcomes = None

    # this function is used to load csv file and process data
    def load_csv_file(self, file_path, selected_date):

        """
        Loads a CSV file and processes its data.
        """
        # hourly data is a dictionary 
        hourly_data = defaultdict(int)
        try:
            # open and read csv file
            with open(file_path, "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # increment count for each hour and junction
                    if row["Date"] == selected_date:
                        hour = row["timeOfDay"].split(":")[0]
                        junction = row["JunctionName"]
                        key = (hour, junction)
                        hourly_data[key] += 1
            return dict(hourly_data)# return data as dictionary
        
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    # this function is used to clear previous data
    def clear_previous_data(self):

        """
        Clears data from the previous run to process a new dataset.
        """
        # clear current data and outcomes 
        self.current_data = None
        self.outcomes = None
        print("\nclear previous data...\n")

    # this function is used to continue or quit the program
    def handle_user_interaction(self):

        """
        Handles user input for processing multiple files.
        """
        # call the function
        return validate_continue_input()

    # this is use to like a main function to process files
    def process_files(self):

        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        # import module and error handling if module not found
        try:
            from functions import validate_date_input, display_outcomes, save_results_to_file
        except ImportError as e:
            print("Error importing module. check the module is available and correctly named")
            raise e
        
        # loop through 
        while True:
            
            # get the user input for date
            day, month, year = validate_date_input(0, 0, 0)
            selected_date = f"{day:02d}/{month:02d}/{year}"
            file_path = f"traffic_data{selected_date.replace('/', '')}.csv"
            
            # load csv file and process data
            self.outcomes = process_csv_data(file_path, selected_date)
            if self.outcomes:
                display_outcomes(self.outcomes)
                save_results_to_file(self.outcomes)
                
                # load csv file and process data using histogram
                self.current_data = self.load_csv_file(file_path, selected_date)
                if self.current_data:
                    histogram = HistogramApp(self.current_data, selected_date)
                    histogram.run()
                    # clear previous data after histogram
                    self.clear_previous_data()
                
            # ask user to continue or quit 
            if not self.handle_user_interaction():
                print("End of run.")
                break

# run the main program
if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()
    
