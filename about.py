#!/usr/local/bin/python3

import pymysql as db
from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie     
from cgi import FieldStorage, escape
from loginText import returnText
from welcome import welcome

returnText   = returnText()
welcomeText  = returnText[1]
buttonText   = returnText[0]
cookie       = SimpleCookie()
cookieHeader = environ.get('HTTP_COOKIE')

print('Content-Type: text/html')
print()
print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Caps by Alexx | About Us</title>
        <link rel="stylesheet" href="styles.css" />
        <link rel="icon" href="images/favicon.ico" type="image/x-icon">        
    </head>  
    <body>
        <header>
            <a href='index.py'><img src='images/noshlogo.png' /></a>
            <form action='showroom.py' method='get'>
                <input type='text' placeholder='Search' name='search'>
                <input type='submit' value='Search'>
            </form>            
            <nav>
                <ul>
                    %s
                    <li><a href='index.py'>Home</a></li>
                    <li><a href='showroom.py'>Showroom</a></li>
                    <li><a href=''>About Us</a></li>
                    <li><a href='login.py'>%s</a></li>
                    <li><a href='cart.py'><img src='images/cart.png'/></a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id='top'>
               <h1>About Us</h1>
            </section>
            <section id='about'>
                <article>
                    <p>sample_text.com</p>
                </article>
            </section>
        </main>
        <footer>
			<small>&copy; Noah Santschi-Cooney. Powered by a crippling addiction to code.</small>        
		</footer>
    </body>  
</html>
""" % (welcomeText, buttonText))
