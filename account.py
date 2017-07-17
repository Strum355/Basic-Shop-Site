#!/usr/local/bin/python3

from os import environ
from http.cookies import SimpleCookie     
from loginText import returnText
import pymysql as db
from shelve import open

cookie       = SimpleCookie()
cookieHeader = environ.get('HTTP_COOKIE')
returnText   = returnText()
welcomeText  = returnText[1]
buttonText   = returnText[0]
output       = ''
count        = 0

try:
    connection = db.connect('localhost', 'username', 'password', 'db')
    cursor     = connection.cursor(db.cursors.DictCursor)

    if cookieHeader:
        cookie.load(cookieHeader)
        if 'sid' in cookie:
            sid = cookie['sid'].value            
            session = open('sessions/session_' + sid, writeback=True)
            if 'auth' in session:
                if 'username' in session:
                    username = session.get('username')    
                    cursor.execute('''SELECT caps.name, caps.pic_link, po.quantity, o.order_date, o.id, caps.price, o.total
                                      FROM product_orders AS po JOIN orders AS o JOIN keycaps AS caps
                                      ON po.id = o.id AND po.product_id = caps.id
                                      WHERE o.username = %s
                                      ORDER BY o.order_date DESC''' , (username))

                    if cursor.rowcount > 0:
                        output = '<article><span><table>'
                        for row in cursor.fetchall():  
                            heading = '' 
                            if count == 0:
                                heading = '<p><b>Order ID:</b> %s</p><p><b>Order Date:</b> %s</p><p><b>Total:</b> &euro;%s</p>' % (row['id'], row['order_date'], row['total'])
                                orderID = row['id']
                                count += 1                       
                            elif row['id'] < orderID:
                                orderID = row['id']
                                output += '</table></span><span><table>'
                                heading = '<p><b>Order ID:</b> %s <p><b>Order Date:</b> %s</p><p><b>Total:</b> &euro;%s</p>' % (row['id'], row['order_date'], row['total'])
                            
                            output += '''%s
                                        <tr>
                                            <td class='image'><img src=%s></td>
                                            <td><p><b>Item:</b> %s</p></td>
                                            <td><p><b>Quantity:</b> %s</p></td>
                                            <td><p><b>Price:</b> &euro;%s</p></td>
                                        </tr>''' % (heading, row['pic_link'], row['name'], row['quantity'], row['price'])

                        output += '</table></article>'
                    else:
                        output = '<article><p>Nothing here! Go buy something <a href="showroom.py">here</a> if you wanna make this place look less empty!</p></article>'
                else:
                    output = '<article><p>Please login</p></article>'               
except db.Error:
    output = '<article><p>Some error message</p></article>'

print('Content-Type: text/html')
print()
print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Caps by Alexx | Account</title>
        <link rel="stylesheet" href="styles.css" />
        <link rel="stylesheet" href="account.css" />
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
               <h1>Your Account</h1>
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
""" % (welcomeText, buttonText, output))
