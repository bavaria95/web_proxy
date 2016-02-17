#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import signal
import thread
import client
from config import *

def init_browser_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if DEBUG:
        # allowing reuse socket, to remove TIME_WAIT TCP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

    sock.bind(('', port))  # '' - to be able to listen all interfaces
    sock.listen(50)

    if DEBUG:
        print('Server has been successfully launched')

    return sock

def processing_request(request, conn):
    print('starting new thread')

    try:
        resp = client.send_request_to_the_server(request, conn)

        if STORE_AND_FORWARD:
            conn.send(resp)
        
        if DEBUG:
            print(resp)
    finally:
        conn.close()


def wait_for_input(sock_browser):
    while True:
        conn, client_addr = sock_browser.accept()
        request = conn.recv(MAX_DATA_RECV)

        if DEBUG:
            print(request)
        
        thread.start_new_thread(processing_request, (request, conn))

def close_socket(sig, frame):
    if sock_browser:
        sock_browser.close()
        if DEBUG:
            print('Socket has been closed')

    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_socket)
    port = 10042
    sock_browser = init_browser_socket(port)
    wait_for_input(sock_browser)

