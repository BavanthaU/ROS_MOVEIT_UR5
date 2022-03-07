# ROS_MOVEIT_UR5
How to test it out:

step 1:
roslaunch robot_environment launch_world.launch

step 2: Then you need to identify hand gesture locations:
rosrun robot_environment image_read.py

step 3: Finally run the user input node:
rosrun robot_environment user_input.py

