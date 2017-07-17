#!/usr/local/bin/python3

import pymysql as db
from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie     
from cgi import FieldStorage, escape
from welcome import welcome
from loginText import returnText
from welcome import welcome

returnText = returnText()
welcomeText = returnText[1]
buttonText  = returnText[0]
checked = [''] * 5
form    = ''
data    = FieldStorage()

try:
    sort = max(min(int(escape(data.getfirst('sort', 0).strip())), 4),0)
except (AttributeError, ValueError):
    sort = 0
checked[int(sort)] = 'checked'

search  = escape(data.getfirst('search','').strip())
output  = ''
sortBy  = {0 : 'price',
           1 : 'price DESC',
           2 : 'name',
           3 : 'name DESC',
           4 : 'stock DESC'}
form = '''<span><input type='radio' value="0" name='sort' id='0' %s><label for='0'>Price low-high</label></span>
          <span><input type='radio' value="1" name='sort' id='1' %s><label for='1'>Price high-low</label></span>
          <span><input type='radio' value="2" name='sort' id='2' %s><label for='2'>Name asc.</label></span>
          <span><input type='radio' value="3" name='sort' id='3' %s><label for='3'>Name desc.</label></span>
          <span><input type='radio' value="4" name='sort' id='4' %s><label for='4'>Stock</label></span>
          <input type='hidden' name='search' value=%s>''' % (checked[0], checked[1],checked[2],checked[3],checked[4], search)
              
cookie       = SimpleCookie()
cookieHeader = environ.get('HTTP_COOKIE')

try:
    connection = db.connect('localhost', 'username', 'password', 'database')
    cursor     = connection.cursor(db.cursors.DictCursor)
    if search != '':
        cursor.execute("""SELECT * FROM keycaps WHERE name LIKE '%s' ORDER BY %s""" % ('%'+ search + '%', sortBy[sort])) 
    else:
        cursor.execute("""SELECT * FROM keycaps ORDER BY %s""" % (sortBy[sort])) 

    if cursor.rowcount > 0:
        for row in cursor.fetchall():
            if row['stock'] >= 1:
                inStock = 'In stock'
                stock   = 'in'
            else:
                inStock = 'Out of stock'
                stock   = 'out'
            output += '''<article>
                         <a href='template.py?page=%s'><img src='%s' /></a>
                         <p><b>Name:</b> %s </p>
                         <p class='%s'><b> %s </b></p>
                         <p><b>Price: </b>&euro;%s</p></article>''' % (row['id'], row['pic_link'], row['name'], stock, inStock, row['price'])
    else:
        output = '<article><p>Nothing found!</p></article>'


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
        <title>Caps by Alexx | Showroom</title>
        <link rel="stylesheet" href="styles.css" />
        <script src='submit.js'></script>
        <link rel="icon" href="images/favicon.ico" type="image/x-icon">
    </head>  
    <body>
        <header>
            <a href='index.py'><img src='images/noshlogo.png' /></a>
            <form action='showroom.py' method='get'>
                <input type='text' placeholder='Search' name='search' value=%s>
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
                <h1>Showroom</h1>
            </section>
            <section id='mid'>
                <section id='sort'>
                    <form action="showroom.py" method="get" id='myForm'> 
                        <label>Sort by:</label>
                        %s
                    </form>
                </section>
                <section id='show'>
                    %s
                </section>
            </section>
        </main>
        <footer>
			<small>&copy; Noah Santschi-Cooney. Powered by a crippling addiction to code.</small>        
		</footer>
    </body>  
</html>
""" % (search, welcomeText, buttonText, form, output))
