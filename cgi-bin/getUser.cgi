#!/usr/bin/python

import cgi
import psycopg2

import bcrypt

def main():
  print "Content-type:text/html\n\n"

  try:
    # conn = MySQLdb.connect('localhost', "root", "2800", "cs160")
    conn =  psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")

    cursor = conn.cursor()

    formData = cgi.FieldStorage()
    username = formData.getvalue('username')
    userpassword = formData.getvalue('password')
    query = 'SELECT password FROM cs160.user_profile WHERE username=%s'

    cursor.execute(query, (username))
    storedPassword = cur.fetchone()
    if bcrypt.checkpw(userpassword, storedPassword[0]):
      print userpassword + '<br>'
      print "Log in Successs"
    else:
      print 'Log in failed: please check your credentials'

    conn.commit()
    cursor.close()
    conn.close()

  except:
    print "error"

if __name__ == "__main__":
  main()
