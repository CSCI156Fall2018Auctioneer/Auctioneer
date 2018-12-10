# Import Classes
from Client import *
from Server import *

def Main():

    # Track if the user has selected an option
    modeChosen = False
    while not modeChosen:
        # Choose operating mode
        mode = raw_input("Which mode would you like to run? Type client or server:\n\r|>")

        # Ensure they entered one of the choices
        if "CLIENT" in mode.upper() or "SERVER" in mode.upper():
            if "CLIENT" in mode.upper():
                # Client Mode
                print("Chosen client mode!")
                modeChosen = True

                client = Client()
                # TODO Build a menu for functions to test

                """
                print("Client Menu:")
                print("1 - Set Server IP Address")
                print("2 - Set Bidding Chance")
                print("3 - Set Max Bid Price")
                clientChoice = input("Choose from above (1 - 3)\n\r|>")
                """


            elif "SERVER" in mode.upper():
                # Server Mode
                print("Chosen server mode!")
                modeChosen = True
                # Start the server
                server = Server()

        else:
            print("Incorrect choice, try again.")


Main()