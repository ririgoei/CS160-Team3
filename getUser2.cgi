#!/usr/bin/python

import cgi
import psycopg2
#import MySQLdb

import bcrypt

def main():
  print "Content-type:text/html\n\n"

  try:
    # conn = MySQLdb.connect('localhost', "root", "2800", "cs160")
    conn =  psycopg2.connect("dbname='cs160' user='postgres' host='localhost' password='2800'")

    cursor = conn.cursor()


    formData = cgi.FieldStorage()
    username = formData.getvalue('username')
    userpassword = formData.getvalue('password')
    sql = 'select password from user_profile where username=%s'

    cursor.execute(sql, (username,))
    storedPassword = cur.fetchone()
    if bcrypt.checkpw(userpassword, storedPassword[0]):
      print userpassword + '<br>'
      print "Log in Successs"
    else:
      print 'Log in failed'

    conn.commit()
    cursor.close()
    conn.close()

  except:
    print "error"

if __name__ == "__main__":
  main()
