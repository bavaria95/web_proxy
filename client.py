#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import socket
import signal
import helper
from config import *

def send_request_to_the_server(request, conn):
    buf = []

    try:
        if FILTERING_MODE:
            url = request.split('\n')[0].split()[1]
            if helper.is_url_forbidden(url):
                return helper.format_redirect_response()

        # create a socket to connect to the webserver
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host, port = parse_host_and_port(request)
        
        sock_server.connect((host, port)) 


        sock_server.send(request)         # send request to webserver

        # reduced default timeout for waiting data, since it took >2s to 
        # be sure that there is no more data
        sock_server.settimeout(RECV_TIMEOUT)

        # until there is data - receive from server and accumulate in buffer
        while True:
            # receive data from web server
            data = sock_server.recv(MAX_DATA_RECV)
            
            if not data:
                break
            else:
                if STORE_AND_FORWARD:
                    # add to buffer
                    buf.append(data)
                else:
                    conn.send(data)

    except socket.error, e:
        if type(e) != socket.timeout:
            print "Runtime Error:", e
            sys.exit(1)
    except:
        return ''

    finally:
        try:
            if sock_server:
                sock_server.close()
        except:
            pass

    return ''.join(buf)


def parse_host_and_port(request):
    # firstly checking HOST field in headers
    http_host = filter(lambda x: x.lower().startswith('host:'), request.split('\n'))
    
    if http_host:
        host = http_host[0][6: -1]
        if ':' in host:
            host, port = host.split(':')
        else:
            host = host.split(':')[0]
            # default then
            port = 80
        
        if DEBUG:
            print(host)
            print(port)
            print

        return (host, port)


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
