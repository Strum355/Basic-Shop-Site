#!/usr/local/bin/python3

from cgitb import enable 
enable()

from cgi import FieldStorage, escape
import pymysql as db

sortBy  = { 0 : 'price',
            1 : 'price DESC',
            2 : 'name',
            3 : 'name DESC',
            4 : 'stock DESC' }
checked = [''] * 5

print('Content-Type: text/plain')
print()

data = FieldStorage()
try:
    sort = int(escape(data.getfirst('sortBy', 0).strip()))
except (AttributeError, ValueError):
    sort = 0
search = escape(data.getfirst('search', ''))
output = ''
try:
    sort = max(min(sort, 4),0)
    connection = db.connect('localhost', 'username', 'password', 'database')
    cursor     = connection.cursor(db.cursors.DictCursor)
    if search != '':
        cursor.execute("""SELECT * FROM keycaps WHERE name LIKE '%s' ORDER BY %s""" % ('%'+ search + '%', sortBy[sort])) 
    else:
        cursor.execute("""SELECT * FROM keycaps ORDER BY %s""" % (sortBy[sort])) 

    checked[int(sort)] = 'checked'
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
    print(output)
except db.Error:
    print('oops')
