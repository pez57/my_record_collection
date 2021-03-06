import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip
from termcolor import colored
import pandas as pd
from helpers import page_greeting
from constants import (MIN_YEAR, CURRENT_YEAR, MENU_OPTION_VIEW_ALL,
                       MENU_OPTION_SEARCH_COLLECTION, MENU_OPTION_ADD_NEW,
                       MENU_OPTION_DELETE)

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


# ---------------- User Input Menu ----------------
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
        menu_options = pyip.inputMenu([MENU_OPTION_VIEW_ALL,
                                       MENU_OPTION_SEARCH_COLLECTION,
                                       MENU_OPTION_ADD_NEW,
                                       MENU_OPTION_DELETE], numbered=True)
        if menu_options == MENU_OPTION_VIEW_ALL:
            view_all_records()
        elif menu_options == MENU_OPTION_SEARCH_COLLECTION:
            search_collection()
        elif menu_options == MENU_OPTION_ADD_NEW:
            user_data = get_users_new_record()
            add_users_new_record(user_data)
        else:
            delete_a_record()
        print(colored("---------- Thank you for using "
                      "'My Record Collection' ----------\n\n", "cyan"))


# ---------------- View All Records ----------------
def get_all_catalog_records():
    """
    Function to return all records in collection as
    Pandas DataFrame.
    """
    return pd.DataFrame(CATALOG_SPREADSHEET.get_all_records())


def view_all_records():
    """
    Function to display the full record collection as a
    DataFrame in Alphabetical order. Error is printed
    if API data fetch fails.
    """
    print(colored("\nNow printing all records in "
                  "the collection...\n", "green"))
    try:
        df_catalog = get_all_catalog_records()
        print(df_catalog.sort_values("Artist"))
    except gspread.exceptions.APIError as e:
        print(colored("\nThere was a problem fetching the data, "
                      "please try again later.", "red"))


# ---------------- Search The Collection ----------------
def search_collection():
    """
    Function to allow user to search for records based
    on search option. When option is selected user
    can input their search criteria.
    """
    df_catalog = get_all_catalog_records()
    search_options = pyip.inputMenu(["Artist", "Title", "Year", "Genre"],
                                    prompt="Please Select Search Criteria:\n",
                                    numbered=True)

    if search_options == "Artist":
        filter_artist = pyip.inputStr("Enter Artist "
                                      "Name to Search...\n").title()
        filtered_artist = (df_catalog.loc[df_catalog["Artist"] ==
                           filter_artist])
        print(filtered_artist)
    elif search_options == "Title":
        filter_title = pyip.inputStr("Enter Album Title to "
                                     "Search...\n").title()
        filtered_title = (df_catalog.loc[df_catalog["Title"] == filter_title])
        print(filtered_title)
    elif search_options == "Year":
        filter_year = pyip.inputInt("Enter Release Year to Search...\n",
                                    min=MIN_YEAR, max=CURRENT_YEAR)
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
    print(colored("\nTo add a new record to the collection, "
                  "please enter the details below\n", "cyan"))
    add_artist = pyip.inputStr("Enter Artist:\n").title()
    add_title = pyip.inputStr("Enter Title:\n").title()
    add_year = pyip.inputInt("Enter Year of Release:\n",
                             min=MIN_YEAR, max=CURRENT_YEAR)
    add_genre = pyip.inputStr("Enter Genre:\n").title()
    new_record = [add_artist, add_title, add_year, add_genre]
    print(f"You Added: {new_record} to the collection")
    return new_record


def add_users_new_record(user_data: list):
    """
    Updates work sheet with new input data
    """
    print(colored("\nNow updating catalog with new addition...\n", "green"))
    CATALOG_SPREADSHEET.append_row(user_data)
    print(colored("Update successful\n", "green"))


# ---------------- Delete Record Functionality ----------------
def delete_a_record():
    """
    Function to allow user to choose a record to delete
    via index number. They can choose to view indexes
    or continue to input index number.
    """
    print(colored("\nDo you know the index number of the "
                  "record you want to delete?...\n", "cyan"))
    view_index_menu = pyip.inputMenu(["NO, show me the index numbers",
                                     "YES, I know the index number"],
                                     numbered=True)
    if view_index_menu == "NO, show me the index numbers":
        show_index_numbers()
        make_deletion()
    elif view_index_menu == "YES, I know the index number":
        make_deletion()


def show_index_numbers():
    """
    Loops through records and displays current catalog
    entries in Index rows.
    """
    current_entries = get_all_catalog_records()

    for i, row in current_entries.iterrows():
        # Above iterates over pandas DataFrame rows
        print(f"Index: {i}, {row[0]}, {row[1]}, {row[2]}, {row[3]} \n")
        # Above Adds "Index: {number} " to the first row and displays


def make_deletion():
    """
    Function takes user inputed index number and deletes the entry
    from DataFrame and google sheet.
    """
    index_to_delete = pyip.inputInt("Delete Index Number:\n")
    full_catalog = get_all_catalog_records()
    full_catalog.drop(index_to_delete)
    index_to_delete = index_to_delete + 2
    # Above Adds 2 to the sheet cell number to match dataframe index
    print(colored("\nNow deleting entry from catalog...\n", "green"))
    CATALOG_SPREADSHEET.delete_rows(index_to_delete)
    print(colored("Deletion successful\n", "green"))


page_greeting()
user_input_menu()
