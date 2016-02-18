#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *

def get_list_of_forbidden():
    with open('forbidden.txt', 'r') as content_file:
        content = content_file.read()
    
    return map(lambda x: x.lower(), content.split('\n')[ :-1])
    
print(get_list_of_forbidden())
    
