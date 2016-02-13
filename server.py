#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

DEBUG = True

def init_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))  # '' - to be able to listen all interfaces
    sock.listen(1)

    if DEBUG:
        print('Server has been successfully launched')

    return sock

def wait_for_input(sock):
    while True:
        conn, client_addr = sock.accept()
        print(conn)
        print(client_addr)

sock = init_socket(10042)
wait_for_input(sock)
