import socket
import sys
import threading
from objects import *
from time import *
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
        # Highest Bidder
        self.HighestBidder = None

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
                self.SecondsTilStart -= 1
                # Print every 5 seconds
                if (self.SecondsTilStart % 5) == 0:
                    print( str(self.SecondsTilStart) + " seconds left until bidding begins!")
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
                # Get the next item
                itemName, itemQuantity, itemPrice = self.ItemsForSale.pop(0)
                # Sell entire stock
                for i in range(0, itemQuantity, 1):
                    self.SellItem(itemName, itemPrice)


    def BroadCastStart(self):
        # Broadcast to all connected Clients
        for socket in self.Clients.values():
            message = EnumCommands.BROADCAST_START
            socket.send(message.encode())
        # Change the state
        self.State = EnumServerState.SELLING


    def SellItem(self, name, price):

        while 1:
            # Send the Item to all clients
            for clientKey in self.Clients.keys():
                # Get the socket using the client IP:Port as key
                socket = self.Clients[clientKey]
                # Check if the client has requested the item
                requestStr = utils.GetResponseString(socket)
                # Check if the request was sent
                if EnumCommands.REQUEST in requestStr:
                    print("SellItem() : Got Request for the item")
                    threading.Thread(target=self.SellThread, args=(clientKey,socket, name, price,)).start()


    def SellThread(self, client, socket, name, price):
        # Send the Item Name and the price
        message = name + ":" + str(price)
        socket.send(message.encode())
        # Lock to print safely
        self.Lock.acquire()
        print("Sent item {" + name + "} to client: " + client)
        self.Lock.release()
        # Continue to accept their bids, and determine the highest bidder
        while 1:
            # See if they bid
            response = utils.GetResponseString(socket)
            if EnumCommands.BID in response:
                print("Client " + client + " placed a bid!")



    def KillConnections(self):
        for key, c in self.Clients:
            print("Closing Connection for " + key)
            c.close()