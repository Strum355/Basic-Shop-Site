#!/usr/local/bin/python3

from os import environ
from shelve import open
from http.cookies import SimpleCookie     
from time import time
from hashlib import sha256

output       = ''
cookie       = SimpleCookie()
cookieHeader = environ.get('HTTP_COOKIE')

def returnText():
    if not cookieHeader:
        loggedIn = False
        sid = sha256(repr(time()).encode()).hexdigest()
        cookie['sid'] = sid
        print(cookie)
    else:
        cookie.load(cookieHeader)
        if 'sid' not in cookie:
            sid = sha256(repr(time()).encode()).hexdigest()
            cookie['sid'] = sid
            print(cookie)
        else:
            sid = cookie['sid'].value
    
    session = open('sessions/session_' + cookie['sid'].value, writeback=True)

    if 'auth' not in session or session.get('auth') == '0':
        return ['Login/Register','<li>Welcome, guest</li>']
    else:
        return ['Logout','<li>Welcome, <a id="welcome" href="account.py">%s</a></li>' % (session['username'])]