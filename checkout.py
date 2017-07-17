#!/usr/local/bin/python3

from os import environ
from http.cookies import SimpleCookie     
from loginText import returnText
from cgi import FieldStorage, escape
import pymysql as db
import time    
import shelve
import smtplib
from email.mime.text import MIMEText

cookie       = SimpleCookie()
cookieHeader = environ.get('HTTP_COOKIE')
returnText = returnText()
welcomeText = returnText[1]
buttonText  = returnText[0]
data         = FieldStorage()
output       = ''

if cookieHeader:
    cookie.load(cookieHeader)
    if 'sid' in cookie:
        sid      = cookie['sid'].value
        session  = shelve.open('sessions/session_' + sid, writeback=True)
        username = session.get('username')
        total    = session.get('total')
        loggedIn = session.get('auth')
        if loggedIn == '1':
            output = '''<section id='checkout'><fieldset>
                        <form action="checkout.py" method="post">
                            <label for='full_name'>Full Name</label>
                            <input type="text" name="full_name" id='full_name'>

                            <label for='addr_line1'>Address Line 1</label>
                            <input type="text" name="addr_line1" id='addr_line1'>

                            <label for='addr_line2'>Address Line 2</label>
                            <input type="text" name="addr_line2" id='addr_line2'> 

                            <label for='city'>City/Town</label>
                            <input type='text' id='city' name='city'>

                            <label for='county'>County/Region</label>
                            <input type='text' id='county' name='county'>

                            <label for='postcode'>Postcode (if applicable)</label>
                            <input type='text' id='postcode' name='postcode'>

                            <label for='country'>Country</label>
                            <input type='text' id='country' name='country'>

                            <label for='phone'>Phone Number (with country code)</label>
                            <input type='text' id='phone' name='phone'>

                            <label for='email'>E-Mail</label>
                            <input type='text' id='email' name='email'>

                            <input type="submit" value"Buy!">
                        </form>
                    </fieldset></section>'''
            if len(data) != 0:
                full_name  = escape(data.getfirst('full_name', ''))
                addr_line1 = escape(data.getfirst('addr_line1', ''))
                addr_line2 = escape(data.getfirst('addr_line2', ''))
                city       = escape(data.getfirst('city', ''))
                county     = escape(data.getfirst('county', ''))
                postcode   = escape(data.getfirst('postcode', ''))
                country    = escape(data.getfirst('country', ''))
                phone      = escape(data.getfirst('phone', ''))
                email      = escape(data.getfirst('email', ''))
                
                emailMesg  = ''
                fullAddr   = ''
                if full_name != '' and addr_line1 != '' and addr_line2 != '' and city != '' and country != '' and county != '' and phone != '':
				    connection = db.connect('localhost', 'username', 'password', 'database')
                    cursor     = connection.cursor(db.cursors.DictCursor)

                    cursor.execute('''INSERT INTO orders
                                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (full_name, addr_line1, addr_line2, city, county, postcode, country, phone, time.strftime('%Y-%m-%d %H:%M:%S'), '', total, username))
                    connection.commit()
                    fullAddr = '\n'+full_name +' \n '+addr_line1 +'\n'+ addr_line2 +'\n'+ city +'\n'+ county +'\n '+postcode +'\n '+country +'\n'
                    cursor.execute('''SELECT id FROM orders
                                      WHERE username = %s
                                      ORDER BY id DESC
                                      LIMIT 1''', (username))
                    orderID = cursor.fetchone()['id'] 

                    for item in session:
                        qty = session.get(item)
                        cursor.execute("""SELECT * FROM keycaps
                                          WHERE id = %s
                                          ORDER BY name""", (item))
                        if cursor.rowcount > 0:
                            emailMesg += cursor.fetchone()['name']
                        
                            cursor.execute('''INSERT INTO product_orders
                                              VALUES (%s, %s, %s)''', (orderID, item, qty))
                            cursor.execute('''UPDATE keycaps
                                              SET stock = stock - %s
                                              WHERE id = %s''', (int(qty),item))
                            del session[item]
                            connection.commit()
                            
                    cursor.close()
                    connection.close()
                    output = '''<article><p>Congrats on your purchase!</p>
                                         <p>You can check out your previous orders in your <a href="account.py">account page</a></p></article>'''

                    msg = MIMEText( 'You bought %s and it was shipped to %s' % (emailMesg, fullAddr))
                    msg['Subject'] = 'Thanks for your purchase!'
                    msg['From'] = 'noah@santschi-cooney.ch'
                    msg['To'] = email

                    s = smtplib.SMTP('localhost')
                    s.sendmail('noah@santschi-cooney.ch', [email], msg.as_string())
                    s.quit()
                else:
                    output = '<article><p>Please fill out the form</p></article>'
                session.close()
        else:
            output = '<article><p>Please <a href="login.py">login</a></p></article>'


print('Content-Type: text/html')
print()
print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Caps by Alexx | Home</title>
        <link rel="stylesheet" href="styles.css" />
        <link rel="icon" href="images/favicon.ico" type="image/x-icon">        
    </head>  
    <body>
        <header>
            <a href=''><img src='images/noshlogo.png' /></a>
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
               <h1>Keycaps by Alex</h1>
               <p>pretty rad if you ask me</p>

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
