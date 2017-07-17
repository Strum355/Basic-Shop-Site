#!/usr/local/bin/python3

from cgi import FieldStorage, escape
from hashlib import sha256
from time import time
import shelve
from http.cookies import SimpleCookie
import pymysql as db
from os import environ
from loginText import returnText
import re 
import smtplib
from email.mime.text import MIMEText

data = FieldStorage()
buttonText   = 'Login/Register'
headingText  = buttonText
adminLink    = ''
welcomeText  = ''
errorMessage = ''
cookie       = SimpleCookie()
cookieHeader = environ.get('HTTP_COOKIE')
loggedIn     = False
logout       = escape(data.getfirst('logout','').strip())
returnText = returnText()

hintText = '''<ul>
                <li>Username must be at least 3 characters long</li>
                <li>Passwords must contain numbers, letters, be at least 4 characters long and optionally non-alphanumerics.</li>
                <li>E-mail will be used for confirmation e-mails</li>
             </ul>'''

loginForm = '''<section id='login'><fieldset>
                   <form action="login.py" method="post">
                       <label for='name'>Username</label>
                       <input type="text" name="loginName" id='name'>

                       <label for='loginPass'>Password</label>
                       <input type="password" name="loginPass" id='loginPass'>
                            
                       <input type='hidden' name='submitted' value='login'>
                       <input type="submit">
                   </form>
               </fieldset></section>'''

registerForm = '''<section id='register'><fieldset>
                    <form action="login.py" method="post">
                        <label for='regName'>Username</label>
                        <input type="text" name="registerName" id='regName' title='Username should consist of at least 3 letters' pattern="(([^a-zA-Z\n\s]*[a-zA-Z][^a-zA-Z\n\s]*){3,40})">
                        <span id='check'></span>

                        <label for='pass'>Password</label>
                        <input type="password" name="registerPass" id='pass' title='Password too weak' pattern='(?=.*\d)(.*[A-Za-z]).{4,}'>

                        <label for='pass1'>Repeat Password</label>
                        <input type="password" name="registerPass1" title='' id='pass1'> 

                        <label for='email'>Email</label>
                        <input type='email' id='email' name='email'>

                        <input type='hidden' name='submitted' value='register'>
                        <input type="submit">
                    </form>
                </fieldset></section>'''
               
if not cookieHeader:
    loggedIn = False
else:
    cookie.load(cookieHeader)
    if 'sid' in cookie:
        session = shelve.open('sessions/session_' + cookie['sid'].value, writeback=True)
        if 'auth' not in session or session.get('auth') == '0':
            loggedIn = False
        elif session.get('auth') != '0':
            loggedIn   = True
            buttonText = 'Logout'
        session.close()

if logout != 'true':
    welcomeText = returnText[1]
#If no data posted
if not data:
    #if sid = 0 or no/wrong cookie
    if loggedIn:
        loginForm    = '<section id="show"><article><p><a href="login.py?logout=true">Logout here</a></p></article></section>'
        registerForm = ''
        hintText     = ''
        headingText  = 'Logout'
else:
    try:
        formType   = escape(data.getfirst('submitted', '').strip())
	    connection = db.connect('localhost', 'username', 'password', 'database')
        cursor     = connection.cursor(db.cursors.DictCursor)


        if logout != 'true':
            #LOGIN
            if formType == 'login':
                username   = escape(data.getfirst('loginName', '').strip())
                password   = escape(data.getfirst('loginPass', '').strip())
                if username != '' and password != '':
                    hashedPass = sha256(password.encode()).hexdigest()

                    cursor.execute('''SELECT * FROM userbase
                                    WHERE username=%s
                                    AND pass=%s''', (username, hashedPass))
                    
                    if cursor.rowcount == 0:
                        #If username or password dont match
                        errorMessage    = '<article id="show"><p>Username and/or password incorrect!</p></article>'
                    else:
                        #if row with username and password exist
                        if 'sid' not in cookie:
                            sid = sha256(repr(time()).encode()).hexdigest()
                            cookie['sid']  = sid
                        else:
                            sid = cookie['sid'].value

                        print(cookie)
                        session = shelve.open('sessions/session_' + sid, writeback=True)
                        session['username'] = username
                        session['auth']     = '1'
                        if session['username'] == 'admin':
                            adminLink = '<a href="admin.py">Administration</a>'

                        welcomeText   = '<li>Welcome, %s' % (username)
                        hintText      = ''
                        headingText   = 'Logged in!'
                        loginForm     = '<section id="show"><article><p>Welcome back %s! %s</p></article></section>' % (username, adminLink)
                        registerForm  = ''
                        buttonText    = 'Logout'
                        session.close()
                else:
                    errorMessage = '<article id="show"><p>Please fill out the form!</p></article>'

            #REGISTER
            elif formType == 'register':
                username  = escape(data.getfirst('registerName','').strip())
                email     = escape(data.getfirst('email','').strip())
                password  = escape(data.getfirst('registerPass','').strip())
                password1 = escape(data.getfirst('registerPass1','').strip())
				
                if username != '' and email != '' and password != '' and password1 != '':
                    if (password == password1):
                        if re.match(r"(?=.*\d)(.*[A-Za-z]).{4,}", password) and re.match(r"(([^a-zA-Z\n\s]*[a-zA-Z][^a-zA-Z\n\s]*){3,40})", username):
                            cursor.execute('''SELECT * FROM userbase
                                            WHERE username=%s''', (username))
                            if cursor.rowcount > 0:
                                errorMessage    = '<article id="show"><p>Username already taken! <a href=''>Try again</a></p></article>'
                            else:


                                hashedPass     = sha256(password.encode()).hexdigest()
                                cursor.execute("""INSERT INTO userbase
                                                  VALUES (%s, %s, %s)""", (username, email, hashedPass))

                                loginForm      = '<section id="show"><article><p>Welcome aboard, %s!</p></article></section>' % (username)
                                registerForm   = ''
                                welcomeText    = '<li>Welcome, <a id="welcome" href="account.py">%s</a>' % (username)
                                buttonText     = 'Logout'
                                headingText    = 'Welcome!'
                                hintText       = ''

                                sid            = sha256(repr(time()).encode()).hexdigest()
                                cookie['sid']  = sid
                                print(cookie)

                                session        = shelve.open('sessions/session_' + sid, writeback=True)
                                session['username'] = username
                                session['auth'] = '1'
                                session.close()
                                connection.commit()

                                fp = open('email.txt', 'r')
                                msg = MIMEText(fp.read())
                                fp.close()

                                msg['Subject'] = 'Welcome aboard to Alex\'s Keycaps, %s!' % (username)
                                msg['From'] = 'noah@santschi-cooney.ch'
                                msg['To'] = email

                                s = smtplib.SMTP('localhost')
                                s.sendmail('noah@santschi-cooney.ch', [email], msg.as_string())
                                s.quit()
                        else:
                            errorMessage = '<article id="show"><p>Password too weak or username too short/long ;) Stop messing with my site</p></article>'
                    else:
                        errorMessage    = '<article id="show"><p>Passwords dont match! <a href=''>Try again</a></p></article>'
                else:
                    errorMessage = '<article id="show"><p>Please fill out the form!</p></article>'
        else:
            sid = sha256(repr(time()).encode()).hexdigest()
            cookie['sid'] = sid            
            session        = shelve.open('sessions/session_' + sid, writeback=True)
            session['auth'] = '0'

            print(cookie)
            welcomeText = '<li>Welcome, guest</li>'
            buttonText  = 'Login/Register'
            session.close()
        cursor.close()
        connection.close()
    except db.Error:
        loginForm = '<article><p>Error!</p></article>'

print('Content-Type: text/html')
print()
print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Caps by Alexx | Login or Register</title>
        <link rel="stylesheet" href="styles.css" />
        <link rel="icon" href="images/favicon.ico" type="image/x-icon">        
        <link rel="stylesheet" href="login.css" />
        <script src='login.js'></script> 
        <script src='nameCheck.js'></script>         
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
                %s
            </section>
                                %s

            <section id='mid'>
                    %s
                    %s
            </section>
        </main>
        <footer>
			<small>&copy; Noah Santschi-Cooney. Powered by a crippling addiction to code.</small>        
		</footer>
    </body>  
</html>
""" % (welcomeText, buttonText, headingText, hintText, errorMessage, loginForm, registerForm))
