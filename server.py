import socket
import sys
import threading
from objects import *

class Server:
    
    def __init__(self):

        # Symbolic name meaning all available interfaces
        self.host = ''
        # Arbitrary unused port number
        self.port = 8888
        # Set the Server State
        self.state = EnumServerState.REGISTERING
        # Dictionary of Clients, accessed by "IP:Port"
        self.Clients = {}
        # Create the Socket, bind the server, and wait for incoming connections
        self.CreateAndBindSocket()

    def CreateAndBindSocket(self):

        print("Starting Server mode...")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket created')
        except socket.error as msg:
            print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])

        # Bind socket to local host and port
        try:
            self.sock.bind((self.host, self.port))
            print('Socket bind complete')
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        # Start listening on socket
        self.sock.listen(10)
        print('Socket now listening')

        # Continue to handle incoming Client connections
        while 1:
            # wait to accept a connection - blocking call
            conn, addr = self.sock.accept()
            # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            threading.Thread(target=self.ClientThread, args=(conn, addr,)).start()

    # Function for handling connections. This will be used to create threads
    def ClientThread(self, conn, addr):

        # Get the key of this connection
        ipPort = addr[0] + ':' + str(addr[1])
        # Receiving from client
        data = conn.recv(1024)
        # Convert to string
        dataStr = repr(data)

        # Handle Clients Registering with the server
        if EnumClientCommands.REGISTER in dataStr:
            # Sending message to connected client
            response = 'You are registered to begin bidding\n'
            conn.send(response.encode())
            self.Clients[ipPort] = conn
            # Show the client has registerd
            print('Registered bidder from: ' + ipPort)


