"""Simple single-threaded, blocking database server for KirbyBase.

"""
import SocketServer
import time
import datetime
import cPickle

from kirbybase import KirbyBase, KBError

host = ''
port = 44444

# Create an instance of the database.
db = KirbyBase('server')

# DBServer class.
class DBServer(SocketServer.BaseRequestHandler):
    # Handler method for client connection.
    def handle(self):
        print "Connected from", self.client_address

        # While client is connected.
        while True:
            # Get the client's request.
            data = self.request.recv(8192)
            
            # If client disconnects, there will be
            # no more data, so break out of loop.
            if not data:
                break

            try:
                # Execute client request.
                s = eval(data)
            except Exception, errObj:
                # If an exception was raised in KirbyBase, grab
                # the exception instance so we can send it back
                # to the client.
                s = errObj

            # Pickle result of client request in binary format so
            # we can send it across network to client.
            s = cPickle.dumps(s,1)
            
            # First send the length of the result, so that the
            # client will no how much data to expect.
            self.request.sendall(str(len(s)))

            # I had to add this because sometimes the server was
            # sending the length, followed by the actual data so
            # fast, that it was arriving at the client all at once
            # and the client was erroring out because it was trying
            # to read data length and was getting data length
            # immediately followed by the result set, which, of
            # course, doesn't make a nice integer.
            time.sleep(.001)

            # Next, send the result itself.
            self.request.sendall(s)

        # If client has disconnected, close the connection to
        # client.
        self.request.close()
        print "Disconnected from", self.client_address

# Create new instance of socketserver, and wait
# for connections.
srv = SocketServer.TCPServer((host,port),DBServer)
srv.serve_forever()

