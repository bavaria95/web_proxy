#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
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
        host, port = parse_host_and_port(request)
        
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
        if type(e) != socket.timeout:
            print "Runtime Error:", e
            sys.exit(1)
    except:
        return ''

    finally:
        if sock_server:
            sock_server.close()

    return ''.join(buf)

def parse_host_and_port(request):
    request_line = request.split('\n')[0].split()

    url = request_line[1]
    m = re.search('(https?:\/\/)?(w{3}\.)?([^:/]*)[^:]*(:\d+)?', url)
    if DEBUG:
        print(m.group(3))
        print(m.group(4))
        print

    host = m.group(3)

    if m.group(4):
        port = int(m.group(4)[1: ])
    else:
        # default then
        port = 80

    return (host, port)