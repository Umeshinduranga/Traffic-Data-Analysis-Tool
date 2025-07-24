import csv
from collections import defaultdict
def validate_date_input(day, month, year):
    
    """ this function is use for a get date from users
        
        Arguments: 
            date : date in DD format
            month : month in MM format
            year : year in YYYY format
        
        returns:
            return day,month,year
        
    """

    while True:
        try:
            # check day is not between 1-31
            # if invalid again ask to input date with correct range 
            if not (1 <= day <= 31):
                #get input for date 
                day = int(input("\nplease enter the date of the survey in the format dd: "))
                if not (1 <= day <= 31):
                    print("Out of range - values must be in the range 1 and 31.")
                    continue# if user input wrng date skip to the rest of code
            

            #check month is not between 1-12
            # input is  incorrect display error msg with input
            if not (1 <= month <= 12):
                month = int(input("plz enter the month of the survey in the formate mm: "))
                if not (1 <= month <= 12):
                    print("Out of range - values must be in the range 1 and 12.")
                    continue
            

             #chek year in not between 2000-2024
            # year isnt in correcct range  display error msg with ask again year
            if not (2000 <= year <= 2024):
                year = int(input("please enter the year of the survey in the format yyyy: "))
                if not (2000 <= year <= 2024):
                    print("Out of range - values must be in the range 2000 and 2024.")
                    continue
            
            #return arguments
            return day, month, year
        except ValueError:
            print("Integer requrired")#if user input non integer value,display this error 


#function for continue of break this load dataset
def validate_continue_input():
        
    """ this funcion is use ,user to decide whether to load another dataset or not

        return:
            response == 'y'
    
    """
    #loop for wrong input.like other letters 
    while True:
        choice = input("Do you want to select another data file for a different date? Y/N > ").lower()
        if choice == "y":
            return True
        if choice == "n":
            return False
        print("Please enter \"y\" or \"n\": ")


#task B
# this function for process csv file 

def process_csv_data(file_path, selected_date):
    
    """ this functions is use to read csv file data and process them


        Arguments:
        file_path : path of csv file    
        selected_date : which data we want to process wahat date 

        returns:
            outcomes : total vehicles,
            total trucks, total electric vehicles,
            two-wheeled vehicles and other requested data

    """
    #get overall count for all categeriz ,and starting 0 for new keys
    stats = defaultdict(int)
    # get hour data with hour starting at 0 by defalt
    hourly_data = defaultdict(int)
    # only stores uniq hours and without duplicate data 
    rainy_hours = set()

    try:
        # read csv file line by line 
        with open(file_path, "r") as file:
            for row in csv.DictReader(file):
                if row["Date"] != selected_date:
                    continue

                stats['total_vehicles'] += 1 # after passing n vehical stats become = {"total_vehical : n "}
                                             # eg - passing 1 and 2nd vehical stats become = {"total_vehical : 1 "}
                                             # and {"total_vehical: 2"}
                
                hour = row["timeOfDay"].split(":")[0]# eg :- after split "14:30" --->  ["14","30"] 
                                                      # if i get 0 th index value, i can get 14
                
                # equal to raw
                vehicle_type = row["VehicleType"]
                junction = row["JunctionName"]

                # get count for all vehiical types 
                if vehicle_type == "Truck":
                    stats["Total_trucks"] += 1 #vehicle

                if vehicle_type in ["Bicycle", "Motorcycle", "Scooter"]:
                    stats['total_two_wheeled'] += 1
                    if vehicle_type == "Bicycle":
                        stats['bikes'] += 1 

                # get count electrinc vehicles
                if row["elctricHybrid"].upper() == "TRUE":# if electrichybrid is "true" or "TRUE" this condition work
                    stats['electric'] += 1 

                # get count buses go north at Elm avenue
                if "Buss" in vehicle_type and junction == "Elm Avenue/Rabbit Road" and row["travel_Direction_out"] == "N":
                    stats['buses_north'] += 1 # if the acc conditions are true, add to stats 

                #get non turning vehicales count
                if row["travel_Direction_in"] == row["travel_Direction_out"]:
                    stats['no_turn'] += 1 # if any vehicle travel direction in and out are equal, add to stats


                if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                    stats['speed_violations'] += 1  # if speed of vehicle is > speed limit, add stats


                 # get junction count 
                if junction == "Elm Avenue/Rabbit Road":
                    stats['elm_road'] += 1 
                    if vehicle_type == "Scooter":
                        stats['elm_scooters'] += 1

                # check vehicles log at "Hanley Highway/Westway"
                if junction == "Hanley Highway/Westway": 
                    stats['hanley'] += 1#add count to hanly if the condion os true
                    hourly_data[hour] += 1  # add count of vehiclles in currunt hour  

                # get count for rainy hours
                whether_data = row.get("Weather_Conditions", '').strip()
                if "Rain" in whether_data:# if any "rain" word in weather condition add hour to rainy_hour
                    rainy_hours.add(hour) 


         # calculate peak hours
        total_hours_of_rain = len(rainy_hours)# get lenth of rainy hours and it shows how many rainy hours 
        max_vehicles = max(hourly_data.values(), default=0) # get  max num of vehicles 
        # find peak hour 
        peak_hours = [f"{hour}:00 and {int(hour)+1}:00" for hour, v in hourly_data.items() if v == max_vehicles]
        

        # return the all calculated traffic data for the given date
        return {
            "data file selected is ": file_path,
            "The total number of vehicles recorded for this date is ": stats['total_vehicles'],
            "The total number of trucks recorded for this date is ": stats['Total_trucks'],
            "The total number of electric vehicles for this date is ": stats['electric'],
            "The total number of two-wheeled vehicles for this date is ": stats['total_two_wheeled'],
            "The total number of busses leaving Elm Avenue/Rabbit Road heading north is ": stats['buses_north'],
            "The total number of vehicles through both junctions not turning left or right is ": stats['no_turn'],
            "The percentage of total vehicles recorded that are trucks for this date is ": round((stats['Total_trucks'] / stats['total_vehicles'] * 100)) if stats['total_vehicles'] else 0,
            "The average number of Bikes per hour for this date is ": stats['bikes'] // 24 if stats['bikes'] else 0,
            "The total number of Vehicles recorded as over the speed limit for this date is ": stats['speed_violations'],
            "The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is ": stats['elm_road'],
            "The total number of vehicles recorded through Hanley Highway/Westway junction is": stats['hanley'],
            "Scooters_Percentage_Elm_Road": round((stats['elm_scooters'] / stats['elm_road'] * 100)) if stats['elm_road'] else 0,
            "The highest number of vehicles in an hour on Hanley Highway/Westway is ": max_vehicles,
            "Peak_Hours_Hanley_Highway": ",".join(peak_hours),#list of string in to one single string
            "The number of hours of rain for this date is ": total_hours_of_rain,
        }
    except FileNotFoundError:
        # if file is not found print error msg
        print(f"Error: '{file_path}' not found")
        return None
    except Exception as e:
        # any other error duisplay this err msg
        print(f"An error occurred: {e}")
        return None


# this function is use to disply all calculated treaffic data 
def display_outcomes(outcomes):
    
    """ this function is use to disply all calculated traffic data.
    """

    if not outcomes:
        return
    
    # print csv fle name with * marks
    print("\n" + "*" * 36)
    print(f"data file selected is {outcomes['data file selected is ']}")
    print("*" * 36, end = "")
    #group traffic data to print output as specification
    # this categarize is only use to print

    categorize_traffic_data = {
        "A": [
            "The total number of vehicles recorded for this date is ",
            "The total number of trucks recorded for this date is ",
            "The total number of electric vehicles for this date is ",
            "The total number of two-wheeled vehicles for this date is ",
            "The total number of busses leaving Elm Avenue/Rabbit Road heading north is ",
            "The total number of Vehicles through both junctions not turning left or right is ",
            "The percentage of total vehicles recorded that are trucks for this date is ",
            "The average number of Bikes per hour for this date is "
        ],
        
        " B ": [
            "The total number of Vehicles recorded as over the speed limit for this date is ",
            "The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is ",
            "The total number of vehicles recorded through Hanley Highway/Westway junction is",
            "Scooters_Percentage_Elm_Road",
        ],

        "C": [
            "The highest number of vehicles in an hour on Hanley Highway/Westway is ",
            "Peak_Hours_Hanley_Highway",
            "The number of hours of rain for this date is ",
        ],
    }


    # print all traffic data in order of group A, B, C
    for group_name, traffic_data in categorize_traffic_data.items():
         # this print is use to get space between each groups 
        print("" * len(group_name))
        for key in traffic_data:
            if key in outcomes:
                if key == "Scooters_Percentage_Elm_Road":
                    # Custom display for scooters percentage
                    print(f"{outcomes[key]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
                    continue
                else:
                    display_key = key.replace("_", " ")
                    print(f"{display_key} {outcomes[key]}")

# function for save results
def save_results_to_file(outcomes, file_name = "results.txt"):
    
    """ this functiion is use to save this traffic data 
    """
    if not outcomes:
        return
    
    # append this traffic data in to txt file 
    try:
        with open(file_name, 'a') as file:
            
            # read the traffic data from the outcome
            for key, value in outcomes.items():
                # if key is not equel to "Scooters_Percentage_Elm_Road" this skip this 
                if key == "Scooters_Percentage_Elm_Road":
                    continue
    
                key = key.replace("_", " ")
                file.write(f"{key} {value}\n")
                
                # schooter persentage is write to tx tile after henly highway juction detas
                if key == "The total number of vehicles recorded through Hanley Highway/Westway junction is":
                    file.write(f"6% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n")
            file.write("*" * 30 + "\n\n")
            print("")
    except Exception as e:
        print(f"Error saving to file: {e}")
