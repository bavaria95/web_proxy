#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import client
from config import *

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
            resp = client.send_request_to_the_server(request)

            conn.send(''.join(resp))
            if DEBUG:
                print(resp)

        finally:
            conn.close()


sock = init_socket(10042)
wait_for_input(sock)

