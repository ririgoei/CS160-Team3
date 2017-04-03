#!/usr/bin/python

import cgi
import MySQLdb
#from passlib.hash import bcrypt
from datetime import datetime
import bcrypt

print "Content-type:text/html\n\n"

try:
  conn = MySQLdb.connect('localhost', "root", "2800", "cs160")
except:
  print "error"
cur = conn.cursor()


formData = cgi.FieldStorage()
firstname = formData.getvalue('firstname')
lastname = formData.getvalue('lastname')
username = formData.getvalue('username')
userpassword = formData.getvalue('password')
confirmpassword = formData.getvalue('confirmpsw')

if userpassword == confirmpassword:
    hashedpassword = bcrypt.hashpw(userpassword, bcrypt.gensalt())
    cur.execute("insert into user_profile values (%s,%s,%s,%s,%s)", (username,hashedpassword,firstname,lastname, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print "Register Successs"
    print "<br >" + hashedpassword
else:
    print "Password doesn't match"
conn.commit()
cur.close()
conn.close()
