import socket
from objects import *
import utils
import time
import select

class Client(object):

    def __init__(self):

        # Welcome message
        print("Starting Client mode...")

        # Connection Vars
        # self.host = raw_imput("Enter Server IP: ")
        self.Host = 'localhost'
        self.Port = 8888


        # Bidding Chance
        # TODO - SET TO 0.7 BEFORE TURNING IN
        self.BiddingChance = 1.0
        # Current Bid value
        self.CurrentBid = 0
        # Max Bid, based on a percent higher than the item price
        self.MaxBid = 0
        # Bidding Increment
        self.BidIncrement = utils.RandBetween(1, 10)

        # Client State
        self.State = EnumClientState.DISCONNECTED

        try:
            # create an AF_INET, STREAM socket (TCP)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket Created')
        except socket.error as msg:
            print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])

        # Initiate the connection to the server
        self.Connect()
        # Send the Registration Request
        self.Register()
        # Start the bidding Loop
        self.OperationLoop()


    # Returns the Remote IP address when given a hostname.
    def ResolveHostname(self, hostname):

        try:
            remote_ip = socket.gethostbyname(hostname)
            print('Ip address of ' + hostname + ' is ' + remote_ip)
        except socket.error:
            # could not resolve
            print('Hostname could not be resolved')
        
        return remote_ip

    def Connect(self):
        # Connect to remote server
        try:
            self.sock.connect((self.Host, self.Port))
            print('Socket Connected to ' + self.Host)
            # Update internal state
            self.State = EnumClientState.CONNECTED
        except socket.error:
            # Connection failed
            print('Connection failed! Exitting...')
            time.sleep(2)
            exit(1)

    def Register(self):

        try:
            # Send Register command to the server
            self.sock.sendall(EnumCommands.REGISTER.encode())
            print('Message send successfully')
            response = utils.GetResponseString(self.sock)
            print("Server response: " + response)
            # Set State
            self.State = EnumClientState.REGISTERED
        except socket.error:
            # Unable to Register
            print('Unable to Register! Exiting...')
            time.sleep(2)
            exit(1)


    def OperationLoop(self):
        # Continue to maintain connection with the server
        while self.State in [EnumClientState.REGISTERED, EnumClientState.AUCTION_STARTED, EnumClientState.BIDDING, EnumClientState.NOT_BIDDING]:

            # If just Registered, Request the latest Item
            if self.State is EnumClientState.REGISTERED:

                # Wait until the auction starts
                # Listen for the server
                response = utils.GetResponseString(self.sock)

                # See if the client is willing to bid based on chance
                if utils.TryChance(self.BiddingChance):
                    # Request latest Item
                    self.sock.sendall(EnumCommands.REQUEST.encode())
                    print("Asking Server for sale item")

                    # Get the response from the server
                    responseStr = utils.GetResponseString(self.sock)
                    print("Received Item from Server: " + responseStr)
                    # Set the state to start bidding
                    self.State = EnumClientState.BIDDING
                    # Split out the item name and price
                    itemName, itemPrice = responseStr.split(':')
                    # Convert to Int
                    itemPrice = int(itemPrice)
                    # Set the base Bidding price
                    self.CurrentBid = itemPrice
                    # Determine the max bidding price
                    percent = utils.RandFloatBetween(1, 10)
                    self.MaxBid = itemPrice + (itemPrice * percent)
                    print("Established Max bidding price of " + str(self.MaxBid))

                else:
                    self.State = EnumClientState.NOT_BIDDING
                    print("Not Bidding on the current item")

            # Bidding State Handler
            if self.State is EnumClientState.BIDDING:
                while 1:
                    if (self.CurrentBid + self.BidIncrement) <= self.MaxBid:
                        # Increase our current bid
                        self.CurrentBid += self.BidIncrement

                        # Send our bid to the server
                        bidMessage = EnumCommands.BID + ":" + str(self.CurrentBid)
                        try:
                            # For some reason this must be resent
                            self.sock.sendall(bidMessage.encode())
                            self.sock.sendall(bidMessage.encode())
                            print("Sent bid for " + str(self.CurrentBid))
                        except socket.error as msg:
                            print('Failed to send bid. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])

                        # Get the response from the server after bidding
                        responseStr = utils.GetResponseString(self.sock)
                        if EnumCommands.HIGHEST_BID in responseStr:
                            print("Woohoo, I have the highest bid!")
                            self.State = EnumClientState.NOT_BIDDING
                            break
                        if EnumCommands.OUTBID in responseStr:
                            print("Outbid by another client! Trying new bid...")
                            continue
                    else:
                        print("Reached max bid on this item! Finished bidding.")
                        self.State = EnumClientState.NOT_BIDDING
                        break


            if self.State is EnumClientState.NOT_BIDDING:
                response = utils.GetResponseString(self.sock)
                # If the current sale closed, we go back to registered, and await a new item
                if EnumCommands.BID_CLOSED in response:
                    print("Item was sold by server, back to waiting for next item")
                    self.State = EnumClientState.REGISTERED
                # If we were outbid, go back to bidding
                if EnumCommands.OUTBID in response:
                    print("Went from Highest Bidder to being Outbid! Jumping back to bidding....")
                    self.State = EnumClientState.BIDDING




