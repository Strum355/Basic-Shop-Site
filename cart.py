#!/usr/local/bin/python3

import pymysql as db
from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie     
from cgi import FieldStorage, escape
from loginText import returnText

name, price, pic_link, link, stock, listOfItems = [],[],[],[],[],[]
totalPrice = 00.00
output, username = '<article><p>Nothing here, folks!</p></article>',"Your"
loggedIn    = False
returnText  = returnText()
welcomeText = returnText[1]
buttonText  = returnText[0]

try:
    cookie       = SimpleCookie()
    cookieHeader = environ.get('HTTP_COOKIE')
    data         = FieldStorage()
    delete       = escape(data.getfirst('delete','').strip())
    updateAmount = escape(data.getfirst('update_amount','').strip())
    itemToDel    = escape(data.getfirst('itemToDel', '').strip())
    updateSubmit = escape(data.getfirst('update', '').strip())
    itemToUpdate = escape(data.getfirst('itemToUpdate', ''))

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
       
    #The session file is opened from the server
    #Which session file is based on the session ID from the cookie
    session = open('sessions/session_'+sid, writeback=True)
    if 'auth' not in session or session.get('auth') == '0':
        loggedIn = False
    elif session.get('auth') != '0':
        loggedIn = True

    #If session file is empty, the person is not logged in and has nothing in cart
    if len(session) != 0:
        #else we connect to the database
	    connection = db.connect('localhost', 'username', 'password', 'database')
        cursor     = connection.cursor(db.cursors.DictCursor)
        
        #If logged in, the cart name is personalised too
        #'___'s cart' instead of 'Your cart'
        if 'username' in session:
            username = session.get('username')+"'s"

        itemsInCart = 0
        output = '<article><table id="cart">'
        for item in sorted(session):
            #returns how many of the current item are in the cart
            qty = session.get(item)

            cursor.execute("""SELECT * FROM keycaps
                              WHERE id = %s
                              ORDER BY name""", (item))

            if cursor.rowcount > 0:
                if itemToDel != '' and item == itemToDel:
                    del session[item] 
                else:
                    itemsInCart += 1 

                    for row in cursor.fetchall():
                        if updateSubmit != '' and item == itemToUpdate:
                            session[item] = min(int(updateAmount), row['stock'])
                            qty = session[item]
                        output += '''<tr>
                                        <td><img src='%s'/></td>
                                        <td><b>Item:</b> %s</td>
                                        <td><b>Price:</b> &euro; %s x %s</td>
                                        <td><form method="post" action="cart.py">
                                                <input type="hidden" value=%s name='itemToDel'>
                                                <input type="submit" name="delete" value="Delete"></form>
                                            <form method="get" action="cart.py">
                                                <input type="submit" name="update" value="Update Cart">
                                                <input type="number" name="update_amount" min=1 max=%s id="update_amount" value=%s>
                                                <input type='hidden' value=%s name='itemToUpdate'>
                                            </form></td>
                                    </tr>''' %(row['pic_link'], row['name'], row['price'], qty, row['id'], row['stock'], qty, row['id'])

                        totalPrice += float(row['price'])*int(qty)
        if itemsInCart == 0:
            output = '<article><p>Nothing here, folks!</p></article>'
        else:
            output += '</table>'
            output += '''<section>
                            <p><b>Total:</b> &euro;%.2f </p>
                         </section>''' % (totalPrice)

            if username != 'Your':
                output += '''<section><p><a href="checkout.py">Finish and Pay</a></p></section></article>'''
            else:
                output += '''<section><p><a href="login.py">Log in or Register to checkout</a></p></section></article>'''
        
        session['total'] = totalPrice
        session.close()
        cursor.close()
        connection.close()
except db.Error:
    output = 'Error!'

print('Content-Type: text/html')
print()
print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Caps by Alexx | Your Cart</title>
        <link rel="stylesheet" href="styles.css"/>
        <link rel="stylesheet" href="cart.css"/>
        <script src='submit.js'></script>        
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
                    <li><a href=''><img src='images/cart.png'/></a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id='top'>
               <h1>%s Cart</h1>
            </section>
            <section id='show'>
                 %s
            </section>
        </main>
        <footer>
			<small>&copy; Noah Santschi-Cooney. Powered by a crippling addiction to code.</small>        
		</footer>
    </body>  
</html>
""" % (welcomeText, buttonText, username, output) )
