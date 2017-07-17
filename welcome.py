#!/usr/local/bin/python3

from cgitb import enable 
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie     
from time import time
from hashlib import sha256

output       = ''
cookie       = SimpleCookie()
cookieHeader = environ.get('HTTP_COOKIE')

def welcome():
    if not cookieHeader:
        loggedIn = False
        sid = sha256(repr(time()).encode()).hexdigest()
        cookie['sid'] = sid
    else:
        cookie.load(cookieHeader)
        if 'sid' not in cookie:
            sid = sha256(repr(time()).encode()).hexdigest()
            cookie['sid'] = sid
        else:
            sid = cookie['sid'].value
    
    session = open('sessions/session_' + cookie['sid'].value, writeback=True)

    if 'auth' not in session or session.get('auth') == '0':
        return '<li>Welcome, guest</li>'
    else:
        return '<li>Welcome, <a href="account.py?user=%s">%s</a></li>' % (session['username'],session['username'])