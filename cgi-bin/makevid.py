#!/usr/bin/python


# makevid :
# 
# This takes one argument, the video id number.
# Saved face data is used to make a modified video
# with triangles drawn on facial landmarks.
# This script should be in Apache cgi-bin.
# 
# Videos are expected to be in /cs160/videos/<#>.mp4
# 
# Frames (color) are expected to be in:
# /cs160/frames/<videoid>/color/<videoid>.<frame#>.png
# 
# List of points are expected to be in:
# /cs160/frames/<videoid>/points/<videoid>.<frame#>.points
# 
# Marked color frames are stored to:
# /cs160/frames/<videoid>/marked/<videoid>.<frame#>.png

import sys
import subprocess
import os
import os.path
import string
import psycopg2

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"

myname = sys.argv[0]
runpath="cgi-bin/"

if ((len(sys.argv) < 2 or  (len(sys.argv) > 2))):
    print "syntax: " + myname + " <video-id#>"
    sys.exit(1)

vidid = sys.argv[1]
videopath = "vids/"
videofile = videopath + vidid + ".mp4"
imgdir = "cgi-bin/frames/color/"

pointsdir = "cgi-bin/frames/points/"

if not os.path.isfile(videofile):
    print "error: video file " + videofile + " not found."
    sys.exit(1)

if not os.path.isdir(imgdir):
    print "error: frames directory " + imgdir + " not found."
    sys.exit(1)

if not os.path.isdir(pointsdir):
    print "error: points directory " + pointsdir + " not found."
    sys.exit(1)

videoid = vidid + ".id"

getcmd = "ffprobe -v 0 -select_streams v:0 -show_entries stream=nb_frames " \
         + videofile + "|grep -v STREAM|cut -f 2 -d="
cur = conn.cursor()
cur.execute("SELECT num_of_frames FROM cs160.video_metadata WHERE video_id = '" + videoid + "';")
nb_frames = cur.fetchone()
print nb_frames[0]

for i in xrange(1,nb_frames[0]):
    # use color frame and set of face points to draw triangles
    # and save as modified frame.

    delcmd = runpath + "delaunay_triangle.py "+vidid+" "+str(i)
    print "delcmd is x " + delcmd + " x"
    subprocess.check_output(delcmd, shell=True)

    print "done triangles for frame " + str(i)

makeVidCmd = "ffmpeg -r 30 -start_number 1 -f image2 -i " + imgdir + vidid + ".%d.tri.png -c:v libx264 cgi-bin/outputvids/" + vidid + "-output.mp4"
a = subprocess.check_output(makeVidCmd, shell=True)