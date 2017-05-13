#!/usr/bin/python


# getoints :
# 
# This takes one argument, the video id number.
# It takes each saved frame image of the video
# and obtains 68 face-points from each, saving
# everything into a separate file for each frame.
# This script should be in Apache cgi-bin.
# 
# Videos are expected to be in /cs160/videos/<#>.mp4
# 
# Frames (grayscale) are expected to be in:
# /cs160/frames/<videoid>/gray/<videoid>.<frame#>.png
# 
# List of points are saved to:
# /cs160/frames/<videoid>/points/<videoid>.<frame#>.points
# 

import sys
import subprocess
import os
import os.path
import string
import psycopg2

myname = sys.argv[0]

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"


cur = conn.cursor()

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

#if not os.path.isdir(pointsdir):
#    os.mkdir(pointsdir)

#getcmd = "ffprobe -v 0 -select_streams v:0 -show_entries stream=nb_frames " \
#         + videofile + "|grep -v STREAM|cut -f 2 -d="
#nb_frames = subprocess.check_output(getcmd, shell=True)

videoid = vidid + ".id"
cur.execute("SELECT num_of_frames FROM cs160.video_metadata WHERE video_id = '" + videoid + "';")
nb_frames = cur.fetchone()
nb_frames = nb_frames[0]

print "please wait...this may take several minutes..."

for i in xrange(1, nb_frames + 1):
    frameid = '{:d}'.format(i)
    imgfile = vidid + "." + frameid + ".png"
    if not os.path.isfile(imgdir + imgfile):
        print "err: frame file " + imgdir + imgfile + " not found."
        sys.exit(2)

    print "Frame number: " + str(i)
    print "Image file: " + imgfile
    tfile = "/tmp/list_det_0.txt"
    
    try:
      getpointscmd = "/home/petr/OpenFace/build/bin/FaceLandmarkImg -f " + imgfile + " -inroot " + imgdir + " -of list.txt -outroot /tmp"
      a = subprocess.check_output(getpointscmd, shell=True)
    except Exception as e:
      print str(e)

    # get pitch/yaw/roll (x/y/z) radian value strings
    yprcmd = "cat " + tfile + "|grep -A 3 ^pose:" \
             + "|grep -v ^pose: |grep -v {|grep -v }"
    yprline = subprocess.check_output(yprcmd, shell=True)

    # (print? or) save yaw/pitch/roll
    (pitch, yaw, roll) = yprline.split(" ")
    print "frame " + str(i) + " yaw, pitch, roll radians = " \
         + yaw +" "+ pitch +" "+ roll
    query = "INSERT INTO cs160.head_position VALUES (%s,%s,%s,%s,%s)"
    cur.execute(query, (str(yaw), str(pitch), str(roll), str(i), videoid))

    file = open("/tmp/list_det_0.txt")
    # save points to file
    pointsfile = pointsdir + vidid + "." + frameid + ".points"
    filep = open(pointsfile, "w")
    query = "INSERT INTO cs160.openface_data VALUES("
    for k,line in enumerate(file):
        if k >= 3 and k < 71:
            x, y = line.split(" ")
            xfloat = (int(float(x)))
            yfloat = (int(float(y)))
            query += str(xfloat) + "," + str(yfloat) + ","
            outline = "%d %d\n" % (xfloat, yfloat)
            filep.write(outline)
            print "k: " + str(k)
            print query + "\n"

    query += str(i) + ",'" + str(videoid) + "');"
    cur.execute(str(query));
    filep.close()
    file.close()

    print "done frame " + frameid

conn.commit()
conn.close()