import socket
import sys
import threading
from objects import *
from time import sleep
import utils

class Server(object):
    
    def __init__(self, secondsToStart=15):

        # Symbolic name meaning all available interfaces
        self.Host = ''
        # Arbitrary unused port number
        self.Port = 8888
        # Set the Server State
        self.State = EnumServerState.REGISTERING


        # Dictionary of Clients, accessed by "IP:Port"
        self.Clients = {}
        # Highest Bidder ( Bidder Key, Bid Amount )
        self.HighestBidder = ("", 0)

        # Mutex Lock
        self.Lock = threading.Lock()

        # Client count to start the bidding
        self.ClientsForBidding = 3
        # Seconds left to start Bidding
        self.SecondsTilStart = secondsToStart


        # List of item tuples
        self.ItemsForSale = []

        # Test Item Triple ( Name , Quantity, Price )
        testItem = ("Item1", 5, 100)
        self.ItemsForSale.append(testItem)

        # Current Item for Sale
        self.CurrentItemIndex = 0
        self.CurrentItem = None

        # Create the Socket, bind the server, and wait for incoming connections
        self.CreateAndBindSocket()

        # Listen for Connections
        self.Listen()

        # Loop while threads handle the work
        self.OperationLoop()

    def CreateAndBindSocket(self):

        print("Starting Server mode...")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket created')
        except socket.error as msg:
            print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])

        # Bind socket to local host and port
        try:
            self.sock.bind((self.Host, self.Port))
            print('Socket bind complete')
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        # Start listening on socket
        self.sock.listen(10)
        print('Socket now listening')

    def Listen(self):

        # Start the Listener
        threading.Thread(target=self.ListenThread, name=EnumThreadNames.LISTENER).start()

        # Start the countdown to begin bidding
        threading.Thread(target=self.CheckReadyToStart, name=EnumThreadNames.CHECKSTART).start()


    def ListenThread(self):
        # Continue to handle incoming Client connections
        while self.State == EnumServerState.REGISTERING:
            # Wait to accept a connection
            conn, addr = self.sock.accept()
            # Name this thread
            threadName = EnumThreadNames.REGISTERCLIENT + str(len(self.Clients))
            # Start a thread to handle registering the client, and updating them with the server states
            threading.Thread(target=self.RegisterClient, args=(conn, addr,), name=threadName).start()

    def CheckReadyToStart(self):
        while self.SecondsTilStart > 0:
            if len(self.Clients) >= self.ClientsForBidding:
                self.State = EnumServerState.BROADCAST_START
            else:
                # Wait one second, and decrease the seconds until start
                sleep(1)
                # Print every 5 seconds
                if (self.SecondsTilStart % 5) == 0:
                    print(str(self.SecondsTilStart) + " seconds left until bidding begins!")
                self.SecondsTilStart -= 1

        if self.SecondsTilStart <= 0:
            self.State = EnumServerState.BROADCAST_START
            print("Bidding has started!")

    # Function for handling connections. This will be used to create threads
    def RegisterClient(self, conn, addr):

        # Get the key of this connection
        ipPort = addr[0] + ':' + str(addr[1])
        # Receiving from client
        dataStr = utils.GetResponseString(conn)

        # If we've started, reject this client
        if self.State in [EnumServerState.BROADCAST_START, EnumServerState.SELLING]:
            response = "You're too late, bidding has started"
            conn.send(response.encode())
            conn.close()
            return

        # Handle Clients Registering with the server
        if EnumCommands.REGISTER in dataStr:
            # Sending message to connected client
            response = 'Registered as client ' + str(len(self.Clients))
            conn.send(response.encode())
            self.Clients[ipPort] = conn
            # Show the client has registerd
            print('Registered bidder from: ' + ipPort)


    def OperationLoop(self):
        while 1:
            # After registration, we broadcast that a new item is going to be sold
            if self.State is EnumServerState.BROADCAST_START:
                self.BroadCastStart()
            # Then we begin selling
            elif self.State is EnumServerState.SELLING:
                if len(self.ItemsForSale) > 0:
                    # Get the next item
                    itemName, itemQuantity, itemPrice = self.ItemsForSale.pop(0)
                    # Sell entire stock
                    for i in range(0, itemQuantity, 1):
                        # Start the timeout for the auction to close
                        threading.Thread(target=self.AuctionTimeout).start()
                        # Start selling this item
                        self.SellItem(itemName, itemPrice)
                        print("SOLD!!! Winner is " + str(self.HighestBidder[0]))
                        sleep(2)
                        # Update all the clients
                        for clientKey in self.Clients.keys():
                            # Get the socket using the client IP:Port as key
                            socket = self.Clients[clientKey]
                            socket.sendall(EnumCommands.AUCTION_CLOSED.encode())
                        self.BroadCastStart()
                else:
                    print("Sold all of our stock! Finished executing..")
                    exit(0)

    def BroadCastStart(self):
        # Broadcast to all connected Clients
        for socket in self.Clients.values():
            message = EnumCommands.BROADCAST_START
            socket.send(message.encode())
        # Change the state
        self.State = EnumServerState.SELLING


    def SellItem(self, name, price):

        # Send the Item to all clients
        for clientKey in self.Clients.keys():
            # Get the socket using the client IP:Port as key
            socket = self.Clients[clientKey]
            # Check if the client has requested the item
            requestStr = utils.GetResponseString(socket)
            # Check if the request was sent
            if EnumCommands.REQUEST in requestStr:
                print("SellItem() : Got Request for the item")
                threading.Thread(target=self.SellThread, args=(clientKey, socket, name, price,)).start()
        # Spin this loop until the auction ends
        while self.State is not EnumServerState.CLOSED:
            x = 1

    def SellThread(self, client, socket, name, price):
        # Send the Item Name and the price
        message = name + ":" + str(price)
        socket.send(message.encode())
        # Lock to print safely
        print("Sent item {" + name + "} to client: " + client)
        # Continue to accept their bids, and determine the highest bidder
        while self.State is not EnumServerState.CLOSED:
            # See if they bid
            response = utils.GetResponseString(socket)
            if EnumCommands.BID in response:
                # Sometimes multiple commands come in, only take the first one
                if len(response.split(':')) > 2:
                    # print(" Had to split the command: " + response)
                    response = '&' + response.split('&')[1]
                    # print("Response now: " + str(response))
                else:
                    # Let the client know we got their bid
                    socket.sendall(EnumCommands.BID_RECEIVED.encode())
                bidCmd, bidAmount = response.split(':')
                bidAmount = int(bidAmount)
                print("Client " + client + " placed a bid for " + str(bidAmount))
                # Lock threads while we examine this bid against the current highest
                self.Lock.acquire()
                if self.HighestBidder[1] < bidAmount:
                    self.HighestBidder = (client, bidAmount)
                    print("Client " + client + " has the highest bid at " + str(bidAmount))
                    # Let them know they are highest bidder
                    message = EnumCommands.HIGHEST_BID
                    socket.send(message.encode())
                else:
                    # Let them know they are outbid
                    message = EnumCommands.OUTBID
                    socket.send(message.encode())
                self.Lock.release()
            # Handle this situation where the request comes in before the thread ended
            if EnumCommands.REQUEST in response:
                socket.send(EnumCommands.RESEND.encode())

    def AuctionTimeout(self):
        secondsLeft = 5
        # Wait 10 seconds for the auction to end
        while secondsLeft > 0:
            sleep(1)
            secondsLeft -= 1
        # Then set the state to Auction Closed
        self.State = EnumServerState.CLOSED

    def KillConnections(self):
        for key, c in self.Clients:
            print("Closing Connection for " + key)
            c.close()