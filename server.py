import socket
import sys
import threading


class Server:
    
    def __init__(self):

        # Symbolic name meaning all available interfaces
        self.host = ''
        # Arbitrary unused port number
        self.port = 8888

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

        # now keep talking with the client
        while 1:
            # wait to accept a connection - blocking call
            conn, addr = self.sock.accept()
            print('Connected with ' + addr[0] + ':' + str(addr[1]))

            # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            connectionThread = threading.Thread(target=self.ClientThread, args=(conn,))
            connectionThread.start()

        s.close()

    # Function for handling connections. This will be used to create threads
    def ClientThread(self, conn):
        # Sending message to connected client
        conn.send(b'Welcome to the server. Type something and hit enter\n')  # send only takes string

        # infinite loop so that function do not terminate and thread do not end.
        while True:

            # Receiving from client
            data = conn.recv(9999)
            reply = 'OK...' + repr(data)
            if not data:
                break

            conn.sendall(reply.encode())

        # came out of loop
        conn.close()


