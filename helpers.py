from termcolor import colored


def page_greeting():
    """
    Display title and welcome messages
    """
    # ACSII art http://patorjk.com/software/taag/
    print("""\n\n\n\n
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
    print(colored("Welcome! In this terminal you can create your own record collection.\n", "green"))
    print(colored("Instructions:\n \
- Please select your option from the numbered menu by typing the corresponding\
\n number and then press enter. This will take you to your desired option.\n", "cyan"))
