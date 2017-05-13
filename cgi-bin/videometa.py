#!/usr/bin/python


## NOTE: This is not functional because the database
## commands are needed to be changed?  Currently this
## script only prints the info to the screen instead
## of executing database commands.


# videometa :
# 
# This takes one argument, the video id number.
# It shows metadata about the input video.
# This script should be in Apache cgi-bin.
# 
# Videos are expected to be in /cs160/videos/<#>.mp4


import sys
import subprocess
import psycopg2
import hashlib

vidid = sys.argv[1]

videopath = "vids/"
videofile = videopath + vidid + ".mp4"

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"

print "video id is = " + vidid

usercmd = "echo `whoami`"
usname = subprocess.check_output(usercmd, shell=True)
usname = usname.split("\n")[0];
print "username is = " + usname


getcmd = "ffprobe -v 0 -select_streams v:0 -show_entries stream=height,width,r_frame_rate,nb_frames " + videofile
print "Getcmd is: " + str(getcmd)
a = subprocess.check_output(getcmd, shell=True)


getcmd = "ffprobe -v 0 -select_streams v:0 -show_entries stream=width " \
         + videofile + "|grep -v STREAM|cut -f 2 -d="
width = subprocess.check_output(getcmd, shell=True)
width = width.split('\n')[0]
print "the width is = " + width

getcmd = "ffprobe -v 0 -select_streams v:0 -show_entries stream=height " \
         + videofile + "|grep -v STREAM|cut -f 2 -d="
height = subprocess.check_output(getcmd, shell=True)
height = height.split('\n')[0]
print "the height is = " + height

getcmd = "ffprobe -v 0 -select_streams v:0 -show_entries stream=r_frame_rate " \
         + videofile + "|grep -v STREAM|cut -f 2 -d="
r_frame_rate = subprocess.check_output(getcmd, shell=True)
r_frame_rate = r_frame_rate.split("/")[0]
print "the r_frame_rate is = " + r_frame_rate

getcmd = "ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 " + videofile
nb_frames = subprocess.check_output(getcmd, shell=True)
print "the nb_frames is = " + nb_frames

videoid = vidid + ".id"
cur = conn.cursor()
query = 'INSERT INTO cs160.video_metadata VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
cur.execute(query, (int(nb_frames), int(width), int(height), int(r_frame_rate), videoid, vidid, videofile, usname))

conn.commit()
conn.close()