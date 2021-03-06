# Import Classes
from client import *
from server import *

def Main():

    # Track if the user has selected an option
    modeChosen = False
    while not modeChosen:
        # Choose operating mode
        print(",,,,,,,,,,,,,,,$$$$")
        print(",,,,,,,,,,,,,,,$$$$")
        print(",,,,,,,,,,,$$$$$$$$$$$$$$$$$")
        print(",,,,,,,$$$$$$$$$$$$$$$$$$$$$$")
        print(",,,,,$$$$$$$,,,,$$$$,,,,$$$$$$$$")
        print(",,,$$$$$$,,,,,,,$$$$,,,,,,,,$$$$$$$")
        print(",,$$$$$$,,,,,,,,$$$$,,,,,,,,,,$$$$$$            Auctioneer")
        print(",,$$$$$$,,,,,,,,$$$$                            CSCI 156 Project")
        print(",,$$$$$$,,,,,,,,$$$$                            Zachary Scott")
        print(",,,$$$$$$,,,,,,,$$$$                            Caleb Tenney") 
        print(",,,,$$$$$$$$,,,,$$$$                            Mason Juarez")
        print(",,,,,,$$$$$$$$$$$$$$$")
        print(",,,,,,,,,,$$$$$$$$$$$$$$$$$")
        print(",,,,,,,,,,,,,,,,,$$$$$$$$$$$$$$$")
        print(",,,,,,,,,,,,,,,,,$$$$,,$$$$$$$$")
        print(",,,,,,,,,,,,,,,,,$$$$,,,,,,,$$$$$$")
        print(",,,,,,,,,,,,,,,,,$$$$,,,,,,,,,,$$$$$")
        print(",,,,,,,,,,,,,,,,,$$$$,,,,,,,,,,,$$$$$")
        print("$$$$$$$,,,,,,,,,,$$$$,,,,,,,,,,,,$$$$$")
        print(",$$$$$$,,,,,,,,,,$$$$,,,,,,,,,,,,$$$$$")
        print(",,$$$$$$$,,,,,,,,$$$$,,,,,,,,,,,$$$$$")
        print(",,,$$$$$$$$,,,,,$$$$,,,,,,,,,,$$$$$")
        print(",,,,,,$$$$$$$$$$$$$$$$$$$$$$")
        print(",,,,,,,,,,$$$$$$$$$$$$$$$$$$$")
        print(",,,,,,,,,,,,,,,,,,$$$$$$$$$$$$")
        print(",,,,,,,,,,,,,,,,,$$$$")
        print(",,,,,,,,,,,,,,,,,$$$$")

        mode = raw_input("Which mode would you like to run? Type client or server:\n\r|>")

        # Ensure they entered one of the choices
        if "CLIENT" in mode.upper() or "SERVER" in mode.upper():
            if "CLIENT" in mode.upper():
                # Client Mode
                print("Chosen client mode!")
                modeChosen = True
                client = Client()


            elif "SERVER" in mode.upper():
                # Server Mode
                print("Chosen server mode!")
                modeChosen = True
                # Start the server
                server = Server(10)

        else:
            print("Incorrect choice, try again.")


Main()