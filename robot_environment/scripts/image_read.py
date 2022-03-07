#!/usr/bin/env python
import os
from webbrowser import get 
import rospy 
from sensor_msgs.msg import Image, CameraInfo 
from cv_bridge import CvBridge 
import cv2 
import cv2.aruco as aruco
import message_filters
import numpy as np
import math
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from std_msgs.msg import String

img_width, img_height = 100, 100

def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return str(dir_path+"/"+path)


path = str(get_path("/hand_gestures_500.h5"))

model = load_model(path)

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
global hand_loc 
hand_loc = ""

pub = rospy.Publisher('hand_location', String,queue_size=100)


def crop_image(points, img):
    minX = img.shape[1]
    maxX = -1
    minY = img.shape[0]
    maxY = -1
    for point in points:

        x = point[0]
        y = point[1]

        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y
    # Now we can crop again just the envloping rectangle
    # finalImage = img[minY:maxY,minX:maxX]
    return round((minX+maxX)/2), round((minY+maxY)/2) 

def initialise_aruco_dictionary():
    global aruco_dict
    aruco_dict = aruco.custom_dictionary(4, 5)
    aruco_dict.markerSize = 5
    aruco_dict.maxCorrectionBits = 3
    aruco_dict.bytesList = np.empty(shape=(4, 4, 4), dtype=np.uint8)

    mybits = np.array([[0, 0, 0, 0, 0],
                       [0, 1, 1, 1, 1],
                       [0, 1, 1, 1, 1],
                       [0, 1, 1, 1, 1],
                       [0, 1, 0, 1, 1]],
                      dtype=np.uint8)
    aruco_dict.bytesList[0] = aruco.Dictionary_getByteListFromBits(mybits)

    mybits = np.array([[0, 0, 1, 1, 1],
                       [1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [1, 1, 0, 0, 0]],
                      dtype=np.uint8)
    aruco_dict.bytesList[1] = aruco.Dictionary_getByteListFromBits(mybits)

    mybits = np.array([[1, 0, 1, 0, 1],
                       [0, 1, 0, 1, 0],
                       [0, 1, 1, 1, 0],
                       [0, 1, 1, 1, 0],
                       [0, 0, 1, 0, 0]],
                      dtype=np.uint8)
    aruco_dict.bytesList[2] = aruco.Dictionary_getByteListFromBits(mybits)

    mybits = np.array([[1, 0, 0, 1, 0],
                       [0, 1, 1, 0, 1],
                       [1, 0, 0, 1, 0],
                       [1, 0, 0, 1, 0],
                       [1, 1, 1, 1, 1]],
                      dtype=np.uint8)
    aruco_dict.bytesList[3] = aruco.Dictionary_getByteListFromBits(mybits)

def callback(rgb_msg, camera_info):
    rgb_image = CvBridge().imgmsg_to_cv2(rgb_msg, desired_encoding="bgr8")
    camera_info_K = np.array(camera_info.K).reshape([3, 3])
    camera_info_D = np.array(camera_info.D)
    h, w = rgb_image.shape[:2]
    newcameramatrix, roi = cv2.getOptimalNewCameraMatrix(camera_info_K, camera_info_D, (w, h), 1, (w, h))
    rgb_undist = cv2.undistort(rgb_image, camera_info_K, camera_info_D, None, newcameramatrix)
    initialise_aruco_dictionary()
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(rgb_undist, aruco_dict, parameters=arucoParams)
    if len(corners) > 0:
        ids = ids.flatten()
        points=[]
        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            # draw the bounding box of the ArUCo detection
            cv2.line(rgb_undist, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(rgb_undist, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(rgb_undist, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(rgb_undist, bottomLeft, topLeft, (0, 255, 0), 2)
            # compute and draw the center (x, y)-coordinates of the ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(rgb_undist, (cX, cY), 4, (0, 0, 255), -1)
            points.append([cX,cY, markerID])
            print("[INFO] ArUco marker ID: {}".format(markerID))
            # show the output image
        imX, imY = crop_image(points, rgb_undist)
        name = get_path("hello.png")
        global hand_loc
        loc = ""
        quadrant = ""
        for i in range(4):
            print(points[i] , imX, imY)
            cX1, cY1, ID = points[i]
            dist = round(math.sqrt((imY-cY1)**2 + (imX-cX1)**2))-150
            print(dist)
            if cX1 > imX and cY1 > imY:
                print("inside 1 ", ID)
                cropped_img = rgb_undist[imY+30:imY+dist, imX+30:imX+dist]
                x,y = (imX+30+imX+dist)/2, (imY+30+imY+dist)/2
                name = get_path("test1.jpg")
                quadrant = "bottom_right"
            elif cX1 > imX and cY1 < imY:
                print("inside 2 ", ID)               
                cropped_img = rgb_undist[cY1+30:cY1+dist, imX+30:imX+dist]  
                x,y = (imX+30+imX+dist)/2, (cY1+30+cY1+dist)/2
                name = get_path("test2.jpg")
                quadrant = "top_right"
            elif cX1 < imX and cY1 > imY:
                print("inside 3 ", ID)
                cropped_img = rgb_undist[imY+30:imY+dist, cX1+30:cX1+dist]  
                x,y = (cX1+30+cX1+dist)/2, (imY+30+imY+dist)/2
                name = get_path("test3.jpg")
                quadrant = "bottom_left"
            elif cX1 < imX and cY1 < imY:
                print("inside 4 ", ID)
                cropped_img = rgb_undist[cY1+30:cY1+dist, cX1+30:cX1+dist]
                x,y = (cX1+30+cX1+dist)/2, (cY1+30+cY1+dist)/2
                name = get_path("test4.jpg")
                quadrant = "top_left"
            print(x,y)
            cv2.circle(rgb_undist, (round(x), round(y)), 8, (0, 0, 255), -1)
            # classes = model.predict(np.expand_dims(cv2.resize(cropped_img,(100,100)), axis=0)) # had a problem 
            cv2.imwrite(name, cropped_img)
            rospy.sleep(1)
            img = image.load_img(name, target_size=(img_width, img_height))
            classes = model.predict(np.expand_dims(img, axis=0))
            print(classes)
            txt1 = str("ArUco " +str(ID) + " marker is having ")
            txt2 = str( "Number " + str(np.argmax(classes[0])) + " hand gesture")
            print(txt1, txt2)
            loc = loc + str(np.argmax(classes[0])) +"|"+ str(x) +":" +str(y) + ":" + quadrant +","
            cv2.putText(rgb_undist, str(txt1),
                (cX1+10, cY1+10), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)
            cv2.putText(rgb_undist, str(txt2),
                (cX1+10, cY1+60), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)
            cv2.waitKey(10)
        cv2.imshow("final_out", rgb_undist)
        cv2.imwrite(get_path("output.jpg"), rgb_undist)
        hand_loc = loc 
        
     

if __name__ == '__main__':
    rospy.init_node('image_processor', anonymous=True)
    image_sub = message_filters.Subscriber('/distorted_camera/link/camera/image', Image)
    info_sub = message_filters.Subscriber('/distorted_camera/link/camera/camera_info', CameraInfo)
    ts = message_filters.ApproximateTimeSynchronizer([image_sub, info_sub], 10, 0.2)
    ts.registerCallback(callback)
    while not rospy.is_shutdown():
        # do whatever you want here
        rospy.loginfo(str(hand_loc))
        pub.publish(str(hand_loc)) 
        rospy.sleep(1)  # sleep for one second

