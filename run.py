import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip
from termcolor import colored
import pandas as pd
import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("record_collection_sheet")
CATALOG_SPREADSHEET = SHEET.worksheet("catalog")


MENU_OPTION_VIEW_ALL = "View All"
MENU_OPTION_SEARCH_COLLECTION = "Search Collection"
MENU_OPTION_ADD_NEW = "Add New"

MIN_YEAR = 1910
CURRENT_YEAR = datetime.datetime.now().year

def page_greeting():
    """
    Display title and welcome messages
    """
    # ACSII art http://patorjk.com/software/taag/
    print("""\n\n\n
        __  ___          ____                                __
       /  |/  /__  __   / __ \ ___   _____ ____   _____ ____/ /
      / /|_/ // / / /  / /_/ // _ \ / ___// __ \ / ___// __  / 
     / /  / // /_/ /  / _, _//  __// /__ / /_/ // /   / /_/ /  
    /_/  /_/ \__, /  /_/ |_| \___/ \___/ \____//_/    \__,_/   
            /____/                                             
       ______        __ __             __   _                  
      / ____/____   / // /___   _____ / /_ (_)____   ____      
     / /    / __ \ / // // _ \ / ___// __// // __ \ / __ \     
    / /___ / /_/ // // //  __// /__ / /_ / // /_/ // / / /     
    \____/ \____//_//_/ \___/ \___/ \__//_/ \____//_/ /_/ 
    """)
                                                         
    print(colored("\nWelcome! In this terminal you can create your own record collection.\n", "green"))
    print(colored("Instructions:\n \
- Please select your option from the numbered menu by typing the corresponding\
\n number and press enter. This will take you to your desired option.\n" , "cyan"))


def user_choice_example():
    """
    This is one way of doing user input validation.
    Another way is using the try except (and ValidationError) concept.
    In the end, pyip achieves all of this in a neat package so this was chosen.
    """
    print("Select an option from below:")
    print(f"1. {MENU_OPTION_VIEW_ALL}")
    print(f"2. {MENU_OPTION_SEARCH_COLLECTION}")
    print(f"3. {MENU_OPTION_ADD_NEW}")
    while True:
        choice = input()
        if choice.isdigit() and int(choice) in [1, 2, 3]:
            # Valid
            return choice
        else:
            print("Please enter a valid choice")

def user_input_menu():
    """
    Display a numbered menu for the user.
    Allows user to navigate to desired option by entering number
    """
    # Run indefinitely
    while True:
        menu_options = pyip.inputMenu([MENU_OPTION_VIEW_ALL, MENU_OPTION_SEARCH_COLLECTION, MENU_OPTION_ADD_NEW], numbered = True)
        if menu_options == MENU_OPTION_VIEW_ALL:
            view_all_records()
        elif menu_options == MENU_OPTION_SEARCH_COLLECTION:
            search_collection()
        else:
            user_data = get_users_new_record()
            add_users_new_record(user_data)
        print(colored("---------- Thank you for using 'My Record Collection' ----------\n\n", "cyan"))

def get_all_catalog_records():
    """
    Function to return all records in collection as
    DataFrame
    """
    return pd.DataFrame(CATALOG_SPREADSHEET.get_all_records())


def view_all_records():
    """
    Function to display the full record collection as a
    DataFrame in Alphabetical order. Error is printed
    if API data fetch fails.
    """    
    print(colored("\nNow printing all records in the collection...\n", "green"))
    try:
        df_catalog = get_all_catalog_records()
        print(df_catalog.sort_values("Artist"))
    except gspread.exceptions.APIError as e:
        print(colored("\nThere was a problem fetching the data, please try again later.", "red"))


def search_collection():
    """
    Function to allow user to search for records based
    on search option. When option is selected user
    can input their search criteria.
    """
    df_catalog = get_all_catalog_records()
    search_options = pyip.inputMenu(["Artist", "Title", "Year", "Genre"], prompt = "Please Select Search Criteria:\n", numbered = True)

    if search_options == "Artist":
        filter_artist = pyip.inputStr("Enter Artist Name to Search...\n").title()
        filtered_artist = (df_catalog.loc[df_catalog["Artist"] == filter_artist])
        print(filtered_artist)
    elif search_options == "Title":
        filter_title = pyip.inputStr("Enter Album Title to Search...\n").title()
        filtered_title = (df_catalog.loc[df_catalog["Title"] == filter_title])
        print(filtered_title)
    elif search_options == "Year":
        filter_year = pyip.inputInt("Enter Release Year to Search...\n", min=MIN_YEAR, max=CURRENT_YEAR)
        filtered_year = (df_catalog.loc[df_catalog["Year"] == filter_year])
        print(filtered_year)
    elif search_options == "Genre":
        filter_genre = pyip.inputStr("Enter Genre to Search...\n").title()
        filtered_genre = (df_catalog.loc[df_catalog["Genre"] == filter_genre])
        print(filtered_genre)

# ---------------- Add New Record Functionality ----------------
def get_users_new_record():
    """
    Function to allow user to add a new record to the collection
    via input catagories.
    """
    print(colored("\nTo add a new record to the collection, please enter the details below\n", "cyan"))
    add_artist = pyip.inputStr("Enter Artist:\n").title()
    add_title = pyip.inputStr("Enter Title:\n").title()
    add_year = pyip.inputInt("Enter Year of Release:\n", min=MIN_YEAR, max=CURRENT_YEAR)
    add_genre = pyip.inputStr("Enter Genre:\n").title()
    new_record = [add_artist, add_title, add_year, add_genre]
    print(new_record)
    return new_record

def add_users_new_record(user_data: list):
    """
    Updates work sheet with new input data
    """
    print(colored("\nNow updating catalog with new addition...\n", "green"))
    CATALOG_SPREADSHEET.append_row(user_data)
    print(colored("Update successful\n", "green"))

page_greeting()
user_input_menu()

