#!/usr/bin/python

import cgi
import sys
import os
import psycopg2
# import MySQLdb
from datetime import datetime
import bcrypt


# Check if user's password matches
def checkPassword(userpassword, confirmpassword):
  if userpassword == confirmpassword:
    return True
  else:
    return False

# Check if username already exist in database
def checkUsername(cursor, conn, username):
  sql = "select username from user_profile where username=%s"
  cursor.execute(sql, (username,))
  name = cursor.fetchall()
  if not name:
    return True
  else:
    return False

# Store user information into database
def storeToDB(cursor, conn, username, userpassword, firstname, lastname):
  hashedpassword = bcrypt.hashpw(userpassword, bcrypt.gensalt())
  sql = "insert into user_profile values (%s,%s,%s,%s,%s,%s)"
  cursor.execute(sql, (username,hashedpassword,firstname,lastname, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(cgi.escape(os.environ["REMOTE_ADDR"]))))
  print "Register Successs"
  print "<br >" + hashedpassword
  print "<br >" + str(cgi.escape(os.environ["REMOTE_ADDR"]))

  conn.commit()
  cursor.close()
  conn.close()

# Main function
def main():
  print "Content-type:text/html\n\n"

  try:
    # conn = MySQLdb.connect('localhost', "root", "2800", "cs160")
    conn =  psycopg2.connect("dbname='cs160' user='postgres' host='localhost' password='2800'")
    cursor = conn.cursor()
    formData = cgi.FieldStorage()
    firstname = formData.getvalue('firstname')
    lastname = formData.getvalue('lastname')
    username = formData.getvalue('username')
    userpassword = formData.getvalue('password')
    confirmpassword = formData.getvalue('confirmpsw')

    if checkPassword(userpassword, confirmpassword) == True:
      if checkUsername(cursor, conn, username) == True:
        storeToDB(cursor, conn, username, userpassword, firstname, lastname)
      else:
        print "\n\nUsername already exist. Please choose another username"
    else:
      print "Password doesn't match"
      sys.exit()


  except:
    print "error"


if __name__ == "__main__":
  main()
