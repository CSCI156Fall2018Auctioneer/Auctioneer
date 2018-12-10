import socket


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
        self.SendData()


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
    def SendData(self):
        # Send some data to remote server
        message = "Hello Server!"

        try:
            # Set the whole string
            self.sock.sendall(message.encode())
            print('Message send successfully')
        except socket.error:
            # Send failed
            print('Send failed')

        response = self.sock.recv(1024)
        print("Server response = " + repr(response))
