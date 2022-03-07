#!/usr/bin/env python3
from multiprocessing.connection import wait
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import actionlib


def move_arm(point):
    # moveit_commander.roscpp_initialize(sys.argv)
    # rospy.init_node('move_arm',
    #                 anonymous=True)

    # robot1_group = moveit_commander.MoveGroupCommander("ur5_arm")
    # robot1_client = actionlib.SimpleActionClient(
    #     'execute_trajectory',
    #     moveit_msgs.msg.ExecuteTrajectoryAction)
    # robot1_client.wait_for_server()
    # rospy.loginfo('Execute Trajectory server is available for robot1')
    # robot1_group.set_named_target(point)
    # _, plan, _, _ = robot1_group.plan()
    # robot1_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
    # robot1_goal.trajectory = plan
    # robot1_client.send_goal(robot1_goal)
    # robot1_client.wait_for_result()
    # rospy.sleep(5)
    # moveit_commander.roscpp_shutdown()
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_arm', anonymous=True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()    
    group = moveit_commander.MoveGroupCommander("ur5_arm")
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1000)

    # group_variable_values = group.get_current_joint_values()

    # group_variable_values[0] = 0
    # group_variable_values[1] = 0
    # group_variable_values[3] = -1.5
    # group_variable_values[5] = 1.5
    # group.set_joint_value_target(group_variable_values)
    group.set_named_target(point)
    _, plan2, _, _ = group.plan()
    plan2 = group.plan()
    group.go(wait=True)

    rospy.sleep(5)

    moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    try:
        print(sys.argv[1])
        move_arm(sys.argv[1])
    except rospy.ROSInterruptException:
        pass