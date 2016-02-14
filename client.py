#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from config import *

def send_request_to_the_server(request):
    buf = []

    try:
        # create a socket to connect to the webserver
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # test server, later would be parsed from headers
        sock_server.connect(('gaia.cs.umass.edu', 80))  
        sock_server.send(request)         # send request to webserver


        # until there is data - receive from server and accumulate in buffer
        while True:
            # receive data from web server
            data = sock_server.recv(MAX_DATA_RECV)
            
            if (len(data) > 0):
                # send back to browser
                buf.append(data)
            else:
                break

    except socket.error, (value, message):
        print "Runtime Error:", message
        sys.exit(1)
    finally:
        if sock_server:
            sock_server.close()

    return buf