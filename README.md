# ROS_MOVEIT_UR5
How to test it out:

step 1: Launch the world with UR5 robot & Moveit planner

roslaunch robot_environment launch_world.launch

step 2: Then you need to identify hand gesture locations:

rosrun robot_environment image_read.py

step 3: Finally run the user input node:

rosrun robot_environment user_input.py

ML Model output --> this is an active node keep predicting the hand locations in real time, so system is capable of handling chnages in the hand locations in real time

![image](https://user-images.githubusercontent.com/70237645/156980285-272726a6-e15e-4c05-a1d0-d6ca9d89c17e.png)
