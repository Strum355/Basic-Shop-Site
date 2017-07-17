#!/usr/local/bin/python3

from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie     
from cgi import FieldStorage, escape
from loginText import returnText
import pymysql as db

returnText = returnText()
welcomeText = returnText[1]
buttonText  = returnText[0]
output, user = '',''
data = FieldStorage()

try:
    cookie       = SimpleCookie()
    cookieHeader = environ.get('HTTP_COOKIE')
    connection   = db.connect('localhost', 'username', 'password', 'database')
    cursor       = connection.cursor(db.cursors.DictCursor)

    itemToAdd    = escape(data.getfirst('item',''))
    try:
        amount = int(escape(data.getfirst('qty','1')))
    except ValueError:
        amount = 1

    if amount and itemToAdd and len(data) != 0:
        cursor.execute("""SELECT stock FROM keycaps
                          WHERE id = %s""" , (itemToAdd))
        if cursor.rowcount > 0:
            
            stock = cursor.fetchone()['stock']

            if stock > 0 and stock >= int(amount) and itemToAdd:
                if not cookieHeader:
                    sid = sha256(repr(time()).encode()).hexdigest()
                    cookie['sid'] = sid
                else:
                    cookie.load(cookieHeader)
                    if 'sid' not in cookie:
                        sid = sha256(repr(time()).encode()).hexdigest()
                        cookie['sid'] = sid 
                    else:
                        sid = cookie['sid'].value
                    
                session = open('sessions/session_' + sid, writeback=True)

                qty = session.get(itemToAdd)
                if not qty:
                    qty = amount
                elif qty + int(amount) <= stock:
                    qty += int(amount)
                    
                session[itemToAdd] = int(qty)
                session.close()
                print(cookie)

                output = '<p>Item successfully added! <a href="cart.py">Check out your cart here!</a> or <a href="showroom.py">continue shopping</a></p>'
            else:
                output = '<p>Item out of stock or too much added to cart!</p>'
        else:
            output = '<p>Nothing to add to cart<p>'
    else:
        output = '<p>Nothing to add to cart<p>'
except IOError:
    output = '<p>Error!</p>'


print('Content-Type: text/html')
print()
print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Keycaps by Alexx</title>
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
                    <li><a href='about.py'>About Us</a></li>
                    <li><a href='login.py'>%s</a></li>
                    <li><a href='cart.py'><img src='images/cart.png'/></a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id='top'>
               <h1>Added to Cart!</h1>

            </section>
            <section id='show'>
                <article>
                    %s
                </article>
            </section>
        </main>
        <footer>
			<small>&copy; Noah Santschi-Cooney. Powered by a crippling addiction to code.</small>        
		</footer>
    </body>  
</html>
""" % (welcomeText, buttonText, output))