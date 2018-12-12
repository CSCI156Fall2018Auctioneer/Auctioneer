import socket
from objects import *
import utils
import time

class Client(object):

    def __init__(self):

        # Welcome message
        print("Starting Client mode...")

        # Connection Vars
        # self.host = raw_imput("Enter Server IP: ")
        self.Host = 'localhost'
        self.Port = 8888

        # Bidding Chance
        self.BiddingChance = 0.3

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
        self.BiddingLoop()


    # Returns the Remote IP address when given a hostname.
    def ResolveHostname(self, hostname):

        try:
            remote_ip = socket.gethostbyname(hostname)
            print('Ip address of ' + hostname + ' is ' + remote_ip)
        except socket.gaierror:
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
            response = self.sock.recv(1024)
            print("Server response: " + repr(response))
            # Set State
            self.State = EnumClientState.REGISTERED
        except socket.error:
            # Send failed
            print('Send failed')


    def BiddingLoop(self):
        # Continue to maintain connection with the server
        while self.State in [EnumClientState.REGISTERED, EnumClientState.BIDDING, EnumClientState.NOT_BIDDING]:

            # Get the response from the server
            response = self.sock.recv(1024)
            # Convert to string
            responseStr = repr(response)

            if EnumCommands.BROADCAST_START in responseStr:
                print("Bidding has Started!")

            # If just Registered, Request the latest Item
            if self.State is EnumClientState.REGISTERED:
                # Request latest Item
                self.sock.sendall(EnumCommands.REQUEST.encode())

                # Get the response from the server
                response = self.sock.recv(1024)
                # Convert to string
                responseStr = repr(response)
            
                print("Recieved Item from Server: " + responseStr)





            # If new, start new bid process
                # Determine if bidding or not
                #
            # else



