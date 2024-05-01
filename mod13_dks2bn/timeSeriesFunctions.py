import numpy as np # type: ignore
import re

def getTimeSeriesFunction(symbol):
    print("\nSelect the time series of the chart you want to generate:")
    print("------------------------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")

    # loops until user chooses a valid time series
    while True:
        choice = input("\nEnter your choice (1-4): ")
        
        # provide interval selection if user selects intraday time series
        if choice == "1":
            while True:
                print("\nSelect the interval for the intraday time series:")
                print("----------------------------------------------------")
                print("1. 1 min")
                print("2. 5 min")
                print("3. 15 min")
                print("4. 30 min")
                print("5. 60 min")
                interval_choice = input("\nEnter your choice (1-5): ")

                intervals = {"1": "1min", "2": "5min", "3": "15min", "4": "30min", "5": "60min"}
                selected_interval = intervals.get(interval_choice)
                if selected_interval:
                    # includes the selected interval in proper api request form for the url in dataFetcher.py
                    return f"TIME_SERIES_INTRADAY&symbol={symbol}&interval={selected_interval}"
                else:
                    print("\nError: Invalid interval. Please select a valid interval (1-5).")

        elif choice in ["2", "3", "4"]:
            functions = {"2": "TIME_SERIES_DAILY", "3": "TIME_SERIES_WEEKLY", "4": "TIME_SERIES_MONTHLY"}
            return functions[choice]
        else:
            print("\nError: Invalid choice. Please select a valid time series (1-4).")
        
        
    # else:
    #     functions = {"2": "TIME_SERIES_DAILY", "3": "TIME_SERIES_WEEKLY", "4": "TIME_SERIES_MONTHLY"}
    #     selected_function = functions.get(choice, "TIME_SERIES_DAILY")  # Default to Daily if invalid choice
    #     if selected_function == "TIME_SERIES_DAILY":
    #         print("Warning: Invalid input detected. Defaulting to Daily time series.")
    #     return selected_function

#testing functions
def validate_symbol_input(symbol: str):
    return len(symbol) >= 1 and len(symbol) <= 7 and symbol.isupper() and symbol.isalpha()

def validate_integer_input(s: str, minimum_inclusive: int, maximum_inclusive: int):
    try:
        value = int(s)
        return value >= minimum_inclusive and value <= maximum_inclusive
    except ValueError:
        return False

def validate_chart_input(chart: str):
    if len(chart) > 1:
        return False
    return validate_integer_input(chart, 1, 2)

def validate_time_series_input(series: str):
    if len(series) > 1:
        return False
    return validate_integer_input(series, 1, 4)

def validate_date_input(date_str: str):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_str):
        return False
    try:
        return np.datetime64(date_str)
    except:
        return False

def validade_symbol_exists(symbol, symbols, symbols_with_description):
    if len(symbol) == 0:
        return False
    if symbol not in symbols:
        print(f"invalid symbol. These are the valid symbols:")
        for symb in symbols_with_description:
            print(symb)
        return False
    return True