import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip
from termcolor import colored
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("record_collection_sheet")
catalog = SHEET.worksheet("catalog")
df_catalog = pd.DataFrame(catalog.get_all_records())

def page_greeting():
    """
    Display title and welcome message
    """
    # ACSII art http://patorjk.com/software/taag/


    print("    __  ___          ____                                __")
    print("   /  |/  /__  __   / __ \ ___   _____ ____   _____ ____/ /")
    print("  / /|_/ // / / /  / /_/ // _ \ / ___// __ \ / ___// __  / ")
    print(" / /  / // /_/ /  / _, _//  __// /__ / /_/ // /   / /_/ /  ")
    print("/_/  /_/ \__, /  /_/ |_| \___/ \___/ \____//_/    \__,_/   ")
    print("        /____/                                             ")
    print("   ______        __ __             __   _                  ")
    print("  / ____/____   / // /___   _____ / /_ (_)____   ____      ")
    print(" / /    / __ \ / // // _ \ / ___// __// // __ \ / __ \     ")
    print("/ /___ / /_/ // // //  __// /__ / /_ / // /_/ // / / /     ")
    print("\____/ \____//_//_/ \___/ \___/ \__//_/ \____//_/ /_/      ")
                                                            

                                                           


    print(colored("\nWelcome! In this terminal you can create your own record collection.\n", "green"))
    print(colored("\nInstructions:\n \
- Please select your option from the numbered menu by typing the corresponding\
\n number and press enter. This will take you to your desired option.\n\
- To return to this section, click the button above the terminal.\n", "cyan"))



def user_inp_menu():
    """
    Display a numbered menu for the user.
    Allows user to navigate to desired option by entering number
    """
    menu_options = pyip.inputMenu(["View All", "Search Collection", "Add New"], numbered = True)

    if menu_options == "View All":
        view_all_records()
    elif menu_options == "Search Collection":
        search_collection()
    else:
        menu_options == "Add New"
        add_new_record()

def view_all_records():
    """
    Function to display the full record collection as a
    list of dictionaries
    """    
    print(colored("\nNow printing all records in the collection...\n", "green"))
    print(df_catalog.sort_values("Artist"))

def search_collection():
    """
    Function to allow user to search for records based
    on search option. When option is selected user
    can input their search criteria.
    """
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
        filter_year = pyip.inputInt("Enter Release Year to Search...\n", min=1910, max=2023)
        filtered_year = (df_catalog.loc[df_catalog["Year"] == filter_year])
        print(filtered_year)
    elif search_options == "Genre":
        filter_genre = pyip.inputStr("Enter Genre to Search...\n").title()
        filtered_genre = (df_catalog.loc[df_catalog["Genre"] == filter_genre])
        print(filtered_genre)


def add_new_record():
    """
    Function to allow user to add a new record to the collection
    via input catagories.
    """
    print(colored("\nTo add a new record to the collection, please enter the details below\n", "cyan"))
    add_artist = pyip.inputStr("Enter Artist:\n").title()
    add_title = pyip.inputStr("Enter Title:\n").title()
    add_year = pyip.inputInt("Enter Year of Release:\n", min=1910, max=2023)
    add_genre = pyip.inputStr("Enter Genre:\n").title()

    new_record = [add_artist, add_title, add_year, add_genre]
    print(new_record)
    return new_record

def update_worksheet(user_data):
    """
    Updates work sheet with new input data
    """
    user_data = add_new_record()
    print(colored("\nNow updating catalog with new addition...\n", "green"))
    catalog.append_row(user_data)
    print(colored("Update successful\n", "green"))


page_greeting()
user_inp_menu()
