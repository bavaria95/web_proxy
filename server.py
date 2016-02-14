#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import signal
import client
from config import *

def init_browser_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', port))  # '' - to be able to listen all interfaces
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

def close_socket(sig, frame):
    print(sig)
    print(frame)

    if sock_browser:
        print('closin socket')
        sock_browser.close()

    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_socket)
    port = 10042
    sock_browser = init_browser_socket(port)
    wait_for_input(sock_browser)

