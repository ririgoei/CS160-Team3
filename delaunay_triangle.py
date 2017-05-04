#!/usr/bin/python
 
import cv2
import numpy as np
import random
import MySQLdb
import sys

db = MySQLdb.connect("127.0.0.1:3306","root","root","cs160");
cursor = db.cursor()
vidid = sys.argv[1]
frameNum = [];
queryFrames = "SELECT num_of_frames FROM video_metadata WHERE video_id="+vidid+";"
cursor.execute(queryFrames)
data = cursor.fetchall()
for data_out in data:
    frameNum.append(data_out[0])

queryWidth = "SELECT x_res FROM video_metadata WHERE video_id="+vidid+";"
queryHeight = "SELECT y_res FROM video_metadata WHERE video_id="+vidid+";"
cursor.execute(queryWidth)
width = cursor.fetchall()
cursor.execute(queryHeight)
height = cursor.fetchall()

# Check if a point is inside a rectangle
def rect_contains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True
 
# Draw a point
def draw_point(img, p, color ) :
    cv2.circle (img, p, 3, color, cv2.cv.CV_FILLED, cv2.LINE_8, 0)
 
 
# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color ) :
 
    triangleList = subdiv.getTriangleList();
    size = img.shape
    r = (0, 0, size[1], size[0])
 
    for t in triangleList :
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])
        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_8, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_8, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_8, 0)
 
if __name__ == '__main__':
 
    # Define window names
    win_delaunay = "Delaunay Triangulation"
 
    # Turn on animation while drawing triangles
    animate = True
     
    # Define colors for drawing.
    delaunay_color = (255,0,0)
    points_color = (0, 0, 255)
 
    # Read in the image.
    img = cv2.imread("rob.png");
     
    # Keep a copy around
    img_orig = img.copy();
     
    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])
     
    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect);
 
    # Create an array of points.
    points = [];
    # Loop data's length; points.append((x[0], y[0]));
    
    x = "x_"
    y = "y_"
    for i in range(1, 68):
        x+=i
        y+=i
        frameNumIndex = frameNum[i]
        cursor.execute("SELECT "+x+","+y+" FROM cs160.openface_data WHERE video_id="+vidid+" AND frame_numbers=" + frameNumIndex + ";")
        data = cursor.fetchall()
        for data_out in data:
            points.append(data_out[0], data_out[1])
 
    # Insert points into subdiv
    for p in points :
        subdiv.insert(p)
         
    # Draw delaunay triangles
    draw_delaunay (img, subdiv, (255, 0, 0));
 
    # Draw points
    for p in points :
        draw_point(img, p, (0,0,255))

    cv2.imwrite("OUTPUT-rob.png", img);