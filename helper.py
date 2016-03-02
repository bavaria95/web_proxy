#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *

def get_list_of_forbidden():
    with open('forbidden.txt', 'r') as content_file:
        content = content_file.read()
    
    return map(lambda x: x.lower(), content.split('\n')[ :-1])

def is_url_forbidden(url):
    '''
    checks whether url doesn't contain forbidden words
    '''
    
    forbidden = get_list_of_forbidden()
    return any(filter(lambda x: x in url.lower(), forbidden))


def format_redirect_response():
    return 'HTTP/1.1 302 Found\r\nLocation: http://www.ida.liu.se/~TDTS04/labs/2011/ass2/error1.html\r\n\r\n'
