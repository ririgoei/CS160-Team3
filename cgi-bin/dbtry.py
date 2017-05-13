import psycopg2
import hashlib

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"


cur = conn.cursor()

#cur.execute("TRUNCATE TABLE cs160.openface_data;")
cur.execute("SELECT * FROM cs160.openface_data;")
#videoid = 'test.id'
#cur.execute("SELECT x_1 FROM cs160.openface_data WHERE frame_numbers = " + str(1) + " AND video_id = '" + videoid + "';")
a = cur.fetchall()
print a
