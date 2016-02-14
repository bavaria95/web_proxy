#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys

DEBUG = True
MAX_DATA_RECV = 4096

def init_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))  # '' - to be able to listen all interfaces
    sock.listen(1)

    if DEBUG:
        print('Server has been successfully launched')

    return sock

def wait_for_input(sock_browser):
    while True:
        conn, client_addr = sock_browser.accept()
        request = conn.recv(MAX_DATA_RECV)
        if DEBUG:
            print(request)
        
        try:
            # create a socket to connect to the webserver
            sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # test server, later would be parsed from headers
            sock_server.connect(('gaia.cs.umass.edu', 80))  
            sock_server.send(request)         # send request to webserver

            # until there is data - receive from server and send to browser
            while True:
                # receive data from web server
                data = sock_server.recv(MAX_DATA_RECV)

                if (len(data) > 0):
                    # send back to browser
                    conn.send(data)
                    if DEBUG:
                        print(data)
                else:
                    break

            sock_server.close()
            conn.close()
        except socket.error, (value, message):
            if sock_server:
              sock_server.close()

            if conn:
              conn.close()

            print "Runtime Error:", message
            sys.exit(1)
    conn.close()


sock = init_socket(10042)
wait_for_input(sock)

