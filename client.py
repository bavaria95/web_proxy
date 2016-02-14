#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import signal
from config import *

def send_request_to_the_server(request):
    buf = []

    try:
        # create a socket to connect to the webserver
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # test server, later would be parsed from headers
        host = 'gaia.cs.umass.edu'
        port = 80
        
        sock_server.connect((host, port))  

        sock_server.send(request)         # send request to webserver

        # reduced default timeout for waiting data, since it took >1s to 
        # be sure that there is no more data
        sock_server.settimeout(RECV_TIMEOUT)
        # until there is data - receive from server and accumulate in buffer
        while True:
            # receive data from web server
            data = sock_server.recv(MAX_DATA_RECV)
            
            if not data:
                break
            else:
                # add to buffer
                buf.append(data)

    except socket.error, e:
        if type(e) == socket.timeout:
            if DEBUG:
                print('timeout')
            return ''.join(buf)
        else:
            print "Runtime Error:", e
            sys.exit(1)

    finally:
        if sock_server:
            sock_server.close()

    return ''.join(buf)
