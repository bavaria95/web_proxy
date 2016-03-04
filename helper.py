#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
import re

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

def format_redirect_response_wrong_url():
    return 'HTTP/1.1 302 Found\r\nLocation: http://www.ida.liu.se/~TDTS04/labs/2011/ass2/error1.html\r\n\r\n'

def format_redirect_response_wrong_content():
    return 'HTTP/1.1 302 Found\r\nLocation: http://www.ida.liu.se/~TDTS04/labs/2011/ass2/error2.html\r\n\r\n'

def is_content_type_presented(pack):
    '''
    checks whether Content-Type field is presented
    '''

    return any(filter(lambda x: x.lower().startswith('content-type: '), pack.split('\r\n')))

def is_searchable_content_type(pack):
    '''
    to make sense analysing text content - it should have "text" content-type
    '''

    content_type = filter(lambda x: x.lower().startswith('content-type: '),
                pack.split('\r\n'))[0][14: ]

    return 'text' in content_type.lower()

def is_content_forbidden(content):
    '''
    checks whether forbidden words occur in the server's response
    '''

    forbidden = get_list_of_forbidden()

    return any(filter(lambda x: x in content.lower(), forbidden))

def ask_for_non_gziped(req):
    '''
    modifies request to the server that it would be without Accept-Encoding field
    if it contained gzip. Needed to ask server to return not gziped response
    to be able to filter it later
    '''

    return '\r\n'.join(filter(lambda x: not x.lower().startswith('accept-encoding: ') and 'gzip' not in x,
          req.split('\r\n')))
