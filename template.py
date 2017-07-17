#!/usr/local/bin/python3

from cgitb import enable 
enable()

import pymysql as db
from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie     
from cgi import FieldStorage, escape
from loginText import returnText

returnText = returnText()
welcomeText = returnText[1]
buttonText  = returnText[0]
title, output = 'Lost?',''
data = FieldStorage()
pageTitle = ''

if len(data) != 0:
    try:
        page       = escape(data.getfirst('page','').strip())
    	connection = db.connect('localhost', 'username', 'password', 'database')
        cursor     = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM keycaps
                          WHERE id = %s""", (page))
        if cursor.rowcount > 0:
            for row in cursor.fetchall():
                pageTitle = row['name']
                if row['stock'] >= 1:
                    stock       = '%s in stock' % (row['stock'])
                    inStock     = 'in'
                    addToBasket = '<input type="number" name="qty" value="1" min=1 max=%s><input type="submit" value="Add to Cart">' % (int(row['stock']))
                else:
                    stock       = 'Out of stock'
                    inStock     = 'out'
                    addToBasket = ''
                
                title   = row['name']
                output += '''<article>
                                <img src='%s' />
                                <p><b>Name:</b> %s </p>
                                <p class='%s'><b> %s </b></p>
                                <form action="addToCart.py" method='post'>
                                    <input type="hidden" value=%s name="item">
                                    %s
                                </form>
                                <p><b>Price: </b> &euro; %i </p>
                                <p id='desc'>%s</p>
                            </article>''' % (row['pic_link'], row['name'], inStock, stock, row['id'], addToBasket, row['price'],row['description'])

        else:
            output = '''<article>
                        <p>Why not play snake while you remember what you were looking for!</p>
                        <script src = 'snake.js' > </script>
                        <canvas width = '500' height = '500'>
                        </canvas></article>'''
        
        cursor.close()
        connection.close()
    except db.Error:
        output = '<p>Error!</p>'

print('Content-Type: text/html')
print()
print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Caps by Alexx | %s</title>
        <link rel="stylesheet" href="styles.css" />
        <link rel="stylesheet" href="product.css" />
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
                <h1>%s</h1>
            </section>
            <section id='product'>
                %s
            </section>
        </main>
        <footer>
            <small>&copy; Noah Santschi-Cooney. Powered by a crippling addiction to code.</small>
        </footer>
    </body>  
</html>
""" % (pageTitle, welcomeText, buttonText, title, output))
