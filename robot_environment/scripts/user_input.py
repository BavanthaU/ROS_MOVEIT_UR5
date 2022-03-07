#!/usr/bin/env python3
import os
import rospy
import moveit_commander
import moveit_msgs.msg
import actionlib
from rospy import init_node, is_shutdown
import rospy
from std_msgs.msg import String

def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return str(dir_path+"/"+path)

def move_arm(loc):
    path = get_path("move_hand.py")
    path = path + " "+loc
    os.system(path)


def callback(data):
    global locations
    locations = {}
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    # 3|497.5:494.5,1|772.0:494.0,2|773.0:219.0,0|497.5:219.5,
    points = data.data.split(",")
    # print(points)
    for point in points:
        if point != '':
            key, val = point.split("|")
            locations[key] = val.split(":")[2]
    # print(locations)

def listener():
    rospy.init_node('user_control', anonymous=True)
    rospy.Subscriber("hand_location", String, callback)


if __name__ == '__main__':
    listener()  
    while not rospy.is_shutdown():
        state = False
        number = input("This program will take robot hand to the chosen number from \n0 \n1 \n2 \n3 \n\nWhere do you want to take the UR5 arm: ")
        if number == "0" or number == "1" or number == '2' or number == '3':
            print ("Ok moving robot arm to Hand Gesture Number " + number+"\n\n\n")
            try:
                print(locations[number])
                move_arm(locations[number])
            except:
                move_arm("home")
                state = True
                print("An exception occurred, Please check whether the arm is at home!") 
        else:
            print("Please enter 0, 1, 2, or 3.\n")
        
        prompt = input("Do you want to try again? (y/n)")
        if prompt == "n" or prompt == "N":
            if not state:
                print("I am going back to home position!")
                move_arm("home")
            break
        else:
            if not state:
                print("I am going back to home position!")
                move_arm("home")
        rospy.sleep(1)  

        