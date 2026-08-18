# -*- coding: utf-8 -*-

"""
Digital Typewriter - تخطيط UK English
"""

UK_LAYOUT = {
    # الصف الأول - @ بدلاً من `
    '@': {'normal': '@', 'shift': '¬'},
    '1': {'normal': '1', 'shift': '!'},
    '2': {'normal': '2', 'shift': '"'},
    '3': {'normal': '3', 'shift': '£'},
    '4': {'normal': '4', 'shift': '$'},
    '5': {'normal': '5', 'shift': '%'},
    '6': {'normal': '6', 'shift': '^'},
    '7': {'normal': '7', 'shift': '&'},
    '8': {'normal': '8', 'shift': '*'},
    '9': {'normal': '9', 'shift': '('},
    '0': {'normal': '0', 'shift': ')'},
    '-': {'normal': '-', 'shift': '_'},
    '=': {'normal': '=', 'shift': '+'},
    
    # الصف الثاني
    'q': {'normal': 'q', 'shift': 'Q'},
    'w': {'normal': 'w', 'shift': 'W'},
    'e': {'normal': 'e', 'shift': 'E'},
    'r': {'normal': 'r', 'shift': 'R'},
    't': {'normal': 't', 'shift': 'T'},
    'y': {'normal': 'y', 'shift': 'Y'},
    'u': {'normal': 'u', 'shift': 'U'},
    'i': {'normal': 'i', 'shift': 'I'},
    'o': {'normal': 'o', 'shift': 'O'},
    'p': {'normal': 'p', 'shift': 'P'},
    '[': {'normal': '[', 'shift': '{'},
    ']': {'normal': ']', 'shift': '}'},
    '\\': {'normal': '\\', 'shift': '|'},
    
    # الصف الثالث
    'a': {'normal': 'a', 'shift': 'A'},
    's': {'normal': 's', 'shift': 'S'},
    'd': {'normal': 'd', 'shift': 'D'},
    'f': {'normal': 'f', 'shift': 'F'},
    'g': {'normal': 'g', 'shift': 'G'},
    'h': {'normal': 'h', 'shift': 'H'},
    'j': {'normal': 'j', 'shift': 'J'},
    'k': {'normal': 'k', 'shift': 'K'},
    'l': {'normal': 'l', 'shift': 'L'},
    ';': {'normal': ';', 'shift': ':'},
    "'": {'normal': "'", 'shift': '"'},
    
    # الصف الرابع
    'z': {'normal': 'z', 'shift': 'Z'},
    'x': {'normal': 'x', 'shift': 'X'},
    'c': {'normal': 'c', 'shift': 'C'},
    'v': {'normal': 'v', 'shift': 'V'},
    'b': {'normal': 'b', 'shift': 'B'},
    'n': {'normal': 'n', 'shift': 'N'},
    'm': {'normal': 'm', 'shift': 'M'},
    ',': {'normal': ',', 'shift': '<'},
    '.': {'normal': '.', 'shift': '>'},
    '/': {'normal': '/', 'shift': '?'},
}