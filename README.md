# Traffic-Data-Analysis-Tool
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/Umeshinduranga/Traffic-Data-Analysis-Tool)

This repository contains a Python-based tool for analyzing traffic survey data from CSV files. The tool processes daily traffic records, calculates a variety of statistics, saves the results, and visualizes the data as an hourly frequency histogram.

## Features

-   **Data Processing**: Reads and parses traffic data from date-specific CSV files.
-   **Statistical Analysis**: Calculates key metrics such as:
    -   Total vehicle counts.
    -   Breakdown by vehicle type (trucks, two-wheelers, electric vehicles).
    -   Speeding violations.
    -   Vehicle counts per junction.
    -   Peak traffic hours.
    -   Percentage of specific vehicle types (e.g., trucks).
    -   Statistics related to weather conditions (e.g., hours of rain).
-   **Data Visualization**: Generates a graphical histogram using Tkinter to display vehicle frequency per hour for the two junctions: `Elm Avenue/Rabbit Road` and `Hanley Highway/Westway`.
-   **Report Generation**: Saves the calculated statistics for each processed date to a `results.txt` file.
-   **Interactive Loop**: Allows the user to analyze data for multiple dates in a single session.

## Project Structure

```
.
└── analysis_tool/
    ├── functions.py              # Core data processing and utility functions
    ├── main_classes.py           # Main application logic, including the GUI and file processing loop
    ├── traffic_data15062024.csv  # Sample traffic data for June 15, 2024
    ├── traffic_data16062024.csv  # Sample traffic data for June 16, 2024
    └── traffic_data21062024.csv  # Sample traffic data for June 21, 2024
```

### File Descriptions

-   **`main_classes.py`**: The entry point for the application. It contains the `MultiCSVProcessor` class to handle the file processing workflow and the `HistogramApp` class to create and manage the Tkinter-based histogram visualization.
-   **`functions.py`**: A module containing all the core logic for reading CSV files (`process_csv_data`), validating user input (`validate_date_input`), displaying results (`display_outcomes`), and saving them to a file (`save_results_to_file`).
-   **`traffic_dataDDMMYYYY.csv`**: CSV files containing the raw traffic data. The file name corresponds to the date of the data within it.

## How to Run

1.  Ensure you have Python installed. The script uses the `tkinter` library, which is included in most standard Python distributions.
2.  Navigate to the `analysis_tool` directory:
    ```bash
    cd analysis_tool
    ```
3.  Run the main script:
    ```bash
    python main_classes.py
    ```
4.  You will be prompted to enter a date for analysis in the format `dd`, `mm`, `yyyy`. Use one of the dates corresponding to the provided CSV files (e.g., 15, 06, 2024).
5.  The script will:
    -   Process the relevant `traffic_data*.csv` file.
    -   Print a detailed statistical summary to the console.
    -   Append these results to `results.txt`.
    -   Open a new window displaying the hourly vehicle frequency histogram.
6.  Close the histogram window to continue.
7.  You will then be asked if you want to analyze another data file. Enter `Y` to process another date or `N` to exit the program.

