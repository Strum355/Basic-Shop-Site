#!/usr/local/bin/python3

from cgi import FieldStorage, escape
import pymysql as db
            
print('Content-Type: text/plain')
print()

data = FieldStorage()
username = escape(data.getfirst('username', '').strip())
try:    
    connection = db.connect('localhost', 'username', 'password', 'database')
    cursor 	   = connection.cursor(db.cursors.DictCursor)
    cursor.execute("""SELECT * FROM userbase 
                      WHERE username = %s""", (username))
    if cursor.rowcount > 0:
        print('taken')
    else:
        print('free')
    cursor.close()  
    connection.close()
except db.Error:
    print('oops')