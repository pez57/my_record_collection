import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip
from termcolor import colored

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

"""
data = catalog.get_all_values()
print(data)
"""

def page_greeting():
    """
    Title and welcome message
    """
    # ACSII art http://patorjk.com/software/taag/
    print("    __  ___         ____                           __   ______      ____          __  _    ")       
    print("   /  |/  /_  __   / __ \___  _________  _________/ /  / ____/___  / / /__  _____/ /_(_)___  ____") 
    print("  / /|_/ / / / /  / /_/ / _ \/ ___/ __ \/ ___/ __  /  / /   / __ \/ / / _ \/ ___/ __/ / __ \/ __ \ ")
    print(" / /  / / /_/ /  / _, _/  __/ /__/ /_/ / /  / /_/ /  / /___/ /_/ / / /  __/ /__/ /_/ / /_/ / / / /")
    print("/_/  /_/\__, /  /_/ |_|\___/\___/\____/_/   \__,_/   \____/\____/_/_/\___/\___/\__/_/\____/_/ /_/ ")
    print("       /____/                                                                                     ")

    print("\nWelcome!\n")
    print("\nInstructions:\n \
- Please select your option from the numbered menu by typing the corresponding\
\n number and press enter. This will take you to your desired option.\n\
- To return to this section, click the button above the terminal.\n")



def user_inp_menu():
    """
    Display a numbered menu for the user.
    Allows user to navigate to desired option by entering number
    """
    menu_options = pyip.inputMenu(["View All", "Search Collection", "Add New"], numbered = True)

    if menu_options == "View All":
        view_all_records()
    

def view_all_records():
    """
    Function to display the full record collection as a
    list of dictionaries
    """
    all_records = catalog.get_all_records()
    print("\nNow printing all records in the collection...\n")
    print(all_records)

def search_for_record():
    """
    Function to allow user to search collection
    via numbered menu of options
    """
    print("\nPlease choose your search criteria from the following options:\n")
    search_options = pyip.inputMenu(["Artist", "Title", "Year", "Genre"], numbered = True)


def add_new_record():
    """
    Function to allow user to add a new record to the collection
    via input catagories
    """
    print("\nTo add a new record to the collection, please enter the details below\n")
    add_artist = pyip.inputStr("Enter Artist: ").capitalize()
    add_title = pyip.inputStr("Enter Title: ").capitalize()
    add_year = pyip.inputInt("Enter Year of Release: ", min=1910, max=2023)
    add_genre = pyip.inputStr("Enter Genre: ").capitalize()

    new_record = [add_artist, add_title, add_year, add_genre]
    print(new_record)

add_new_record()


