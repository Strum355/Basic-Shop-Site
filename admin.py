#!/usr/local/bin/python3

import cgi, os

from cgi import FieldStorage, escape
from hashlib import sha256
from time import time
import shelve
from http.cookies import SimpleCookie
import pymysql as db
import os
from welcome import welcome
from loginText import returnText

print('Content-Type: text/html')
print()

returnText = returnText()
welcomeText = returnText[1]
buttonText  = returnText[0]
insert      = ''
authorized  = False
buttonText  = 'Login/Register'
try:
    cookie       = SimpleCookie()
    cookieHeader = os.environ.get('HTTP_COOKIE')
    data         = FieldStorage()
    submitType   = escape(data.getfirst('type','').strip())
    delete       = escape(data.getfirst('delete','').strip())

    if not cookieHeader:
        pass
    else:
        cookie.load(cookieHeader)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session = shelve.open('sessions/session_' + sid, writeback=True)
            if 'username' in session:
                username = session.get('username')    
                if username == 'admin':
                    authorized = True
        if 'auth' not in cookie or cookie['auth'].value == '0':
            pass
        elif cookie['auth'].value != '0':
            buttonText = 'Logout'

    if authorized:
        if len(data) != 0:
            if submitType != '' and submitType == 'input':
                name   = escape(data.getfirst('name','').strip())
                price  = escape(data.getfirst('price','').strip())
                desc   = escape(data.getfirst('description','').strip())
                image  = data['image']

                fileName = 'images/'+image.filename
                open(fileName, 'wb').write(image.file.read())
                os.chmod(fileName, 604)

   				connection = db.connect('localhost', 'username', 'password', 'database')
                cursor     = connection.cursor(db.cursors.DictCursor)

                cursor.execute("""INSERT INTO keycaps
                                VALUES (%s, %s, %s, %s, %s, %s)""", (name, price, True, fileName, '', desc))
                connection.commit()

                insert = '<article><p>Successfully added! <a href="admin.py">Go back to Admin page</a></p></article>'
                cursor.close()
                connection.close()
            elif submitType != '' and submitType == 'update':
                idValue      = escape(data.getfirst('id','').strip())
                updateAmount = escape(data.getfirst('update_amount','').strip())

			    connection = db.connect('localhost', 'username', 'password', 'database')
                cursor     = connection.cursor(db.cursors.DictCursor)
                cursor.execute('''UPDATE keycaps
                                  SET stock = %s
                                  WHERE id = %s''', (updateAmount,idValue))
                connection.commit()
                insert = '<article><p>Successfully updated! <a href="admin.py">Go back to Admin page</a></p></article>'
                cursor.close()
                connection.close()
            elif delete != '':
                idValue      = escape(data.getfirst('id','').strip())

			    connection = db.connect('localhost', 'username', 'password', 'database')
                cursor     = connection.cursor(db.cursors.DictCursor)
                cursor.execute('''DELETE FROM keycaps
                                  WHERE id = %s''', (idValue))
                connection.commit()
                insert = '<article><p>Successfully deleted! <a href="admin.py">Go back to Admin page</a></p></article>'
                cursor.close()
                connection.close()
        else: 
    		connection = db.connect('localhost', 'username', 'password', 'database')
            cursor     = connection.cursor(db.cursors.DictCursor)
            cursor.execute('''SELECT * FROM keycaps''')

            insert = '''<article><form action='admin.py' method='post' enctype='multipart/form-data'>
                            <label for='name'cart.py>Name:</label>
                            <input type='text' maxlength='20' id='name' name='name'>

                            <label for='price'>Price:</label>
                            <input type='text' id='price' name='price' title='Must contain numbers only' pattern='[0-9]+(\\.[0-9][0-9]?)?'>

                            <label for='image'>Image (file name length under 37 chars):</label>
                            <input type='file' id='image' name='image' accept='image/*'>

                            <label for='description'>Description:</label>
                            <textarea id='description' name='description' rows='10' cols='50'></textarea>

                            <input type='hidden' value='input' name='type'>
                            <label for='submit'>Submit</label>
                            <input type='submit' id='submit'>
                        </form></article>'''
            if cursor.rowcount > 0:
                insert += '<article><table>'
                for row in cursor.fetchall():
                    insert += '''<tr>
                                    <td><img src='%s'/></td>
                                    <td><b>Item:</b> %s</td>
                                    <td><form method="get" action="admin.py">
                                            <input type="submit" name="update" value="Update amount">
                                            <input type="number" name="update_amount" min=0 id="update_amount" value=%s>
                                            <input type='hidden' name='type' value='update'>
                                            <input type='hidden' name='id' value=%s></form>
                                        <form method='get' action='admin.py'>         
                                            <input type='hidden' name='id' value=%s>                                                                       
                                            <input type='submit' name='delete' value='Delete'></form></td>
                                </tr>''' %(row['pic_link'], row['name'], row['stock'], row['id'],row['id'])
                insert += '</table></article>'
    else:   
        insert = '<article><p>Not authorized!</p></article>'

except db.Error:
    insert = 'Error!'

print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Caps by Alexx | Administration</title>
        <link rel="stylesheet" href="styles.css" />
        <link rel="stylesheet" href="admin.css" />
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
               <h1>Administration</h1>
               <p>DONT PRESS THE RED BUTTON</p>

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
""" % (welcomeText, buttonText, insert))
