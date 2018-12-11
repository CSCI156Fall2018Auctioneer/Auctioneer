import socket
from objects import *

class Client:

    def __init__(self):

        # Declare class vars
        self.host = 'localhost'
        self.port = 8888

        print("Starting Client mode...")

        try:
            # create an AF_INET, STREAM socket (TCP)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket Created')
        except socket.error as msg:
            print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])

        # Initiate the connection to the server
        self.Connect()
        self.Register()


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
        self.sock.connect((self.host, self.port))
        print('Socket Connected to ' + self.host)


    # To be called outside
    def Register(self):

        try:
            # Send Register command to the server
            self.sock.sendall(EnumClientCommands.REGISTER.encode())
            print('Message send successfully')
        except socket.error:
            # Send failed
            print('Send failed')

        response = self.sock.recv(1024)
        print("Server response: " + repr(response))
