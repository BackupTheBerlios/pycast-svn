"""Threaded, non-blocking database server for KirbyBase.

Each client request runs in its own thread.  Threads only block when
attempting to open a table file in 'w' or 'r+' mode and the table
is already opened in one of these modes.
"""
import re
import SocketServer
import threading
import time
import datetime
import cPickle

from kirbybase import KirbyBase, KBError

host = ''
port = 44444

# Setup a dictionary to hold a thread lock for each table.
WriteLocks = {}

# Compile a regular expression to look for a client request that needs to
# write to the database.
update_pattern = re.compile(
 'db.update|db.delete|db.insert|db.pack|db.drop')

# DBServer class.
class DBServer(SocketServer.BaseRequestHandler):
    # Handler method for client connection.
    def handle(self):
        print "Connected from", self.client_address

        # Create an instance of the database.  I execute this statment
        # within the handle, so that each connection thread will have
        # it's own instance of the database.  This prevents threads
        # from writing over each other's instance variables.
        db = KirbyBase('server')

        # While client is connected.
        while True:
            # Get the client's request.
            data = self.request.recv(8192)

            # If client disconnects, there will be no more data, so break
            # out of loop.
            if not data:
                break

            # If this client request needs to write to the database, set
            # a flag to true and try to acquire the lock, blocking until
            # it is released.  This won't block the other threads, though,
            # since we specified a 'ThreadingTCPServer'.
            if re.match(update_pattern, data):
                need_to_write = True
                tbl = data.split("'")[1]

                # If no process has asked for a lock in this table, yet,
                # then create a lock and put it in the dictionary before
                # trying to acquire it.
                if not WriteLocks.has_key(tbl):
                    print "Creating lock for", tbl
                    WriteLocks[tbl] = threading.Lock()

                WriteLocks[tbl].acquire()
            else:
                need_to_write = False

            try:
                # Execute client request.
                s = eval(data)
            except Exception, errObj:
                # If an exception was raised in KirbyBase, grab
                # the exception instance so we can send it back
                # to the client.
                s = errObj

            # If this request acquired the lock, release the lock.
            if need_to_write:
                WriteLocks[tbl].release()

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

        # If client has disconnected, close the connection to client.
        self.request.close()
        print "Disconnected from", self.client_address

# Create new instance of socketserver, and wait for connections.
srv = SocketServer.ThreadingTCPServer((host,port),DBServer)
#srv.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
srv.serve_forever()

