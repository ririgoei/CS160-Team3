#!/usr/bin/python

import cgi
import MySQLdb
#from passlib.hash import bcrypt
import bcrypt

print "Content-type:text/html\n\n"

try:
  conn = MySQLdb.connect('localhost', "root", "2800", "cs160")
except:
  print "error"
cur = conn.cursor()


formData = cgi.FieldStorage()
username = formData.getvalue('username')
userpassword = formData.getvalue('password')

cur.execute('select password from user_profile where username=%s', (username,))
storedPassword = cur.fetchone()
if bcrypt.checkpw(userpassword, storedPassword[0]):
  print userpassword + '<br>'
  print "Log in Successs"
else:
  print 'Log in failed'

conn.commit()
cur.close()
conn.close()
