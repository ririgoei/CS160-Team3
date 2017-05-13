#!/usr/bin/python

import cgi
import sys
import os
import psycopg2
from datetime import datetime
import bcrypt


# Check if user's password matches
def checkPassword(userpassword, confirmpassword):
  return userpassword == confirmpassword
  #   return True
  # else:
  #   return False

# Check if username already exist in database
def checkUsername(cursor, conn, username):
  query = "SELECT username FROM cs160.user_profile WHERE username=%s"
  cursor.execute(query, (username,))
  name = cursor.fetchall()
  if not name:
    return True
  else:
    return False

# Store user information into database
def storeToDB(cursor, conn, username, userpassword, firstname, lastname):
  hashedpassword = bcrypt.hashpw(userpassword, bcrypt.gensalt())
  query = "INSERT INTO cs160.user_profile VALUES (%s,%s,%s,%s,%s,%s)"
  cursor.execute(query, (username,hashedpassword,firstname,lastname, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(cgi.escape(os.environ["REMOTE_ADDR"]))))
#  print "Register Successs"
# print "<br >" + hashedpassword
#  print "<br >" + str(cgi.escape(os.environ["REMOTE_ADDR"]))

  conn.commit()
  cursor.close()
  conn.close()

# Main function
def main():
  print "Content-type:text/html\n\n"

  try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
#    print "Connected to database!"
  except:
    print "I am unable to connect to the database"

  cur = conn.cursor()
  formData = cgi.FieldStorage()
  firstname = formData.getvalue('firstname')
  lastname = formData.getvalue('lastname')
  username = formData.getvalue('username')
  userpassword = formData.getvalue('password')
  confirmpassword = formData.getvalue('confirmpsw')

  if checkPassword(userpassword, confirmpassword):
    try:
      if checkUsername(cur, conn, username):
        try:
          storeToDB(cur, conn, username, userpassword, firstname, lastname)
          redirect()
        except Exception as e: 
          print str(e)
      else:
        print "\n\nUsername already exist. Please choose another username"
    except Exception as e:
      print e
  else:
    print "Password doesn't match"
    sys.exit()

def redirect():
    print "<script>window.location = \"http://localhost/registercomplete.html\";</script></body></html>"

if __name__ == "__main__":
  main()
