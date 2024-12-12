#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class GoalNavigator:
    def __init__(self):
        # MoveBase client setup
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

        # Hedef konumları (X, Y)
        self.goals = [
            (2.263212297205351, 0.04858943636032197),  # 1. hedef
            (4.321309353173513, 2.1247760211114644),  # 2. hedef
            (-1.1624015980814437, 2.7063710502841323)  # 3. hedef
        ]

        self.current_goal_index = 0

    def send_goal(self, goal):
        """Belirli bir hedefe gitmek için MoveBase komutunu gönder"""
        goal_x, goal_y = goal

        # Move Base hedefini oluşturun
        move_goal = MoveBaseGoal()
        move_goal.target_pose.header.frame_id = "map"
        move_goal.target_pose.header.stamp = rospy.Time.now()
        move_goal.target_pose.pose.position.x = goal_x
        move_goal.target_pose.pose.position.y = goal_y
        move_goal.target_pose.pose.orientation.w = 1.0

        rospy.loginfo(f"Yeni hedef gönderiliyor: {goal_x}, {goal_y}")
        self.client.send_goal(move_goal)
        self.client.wait_for_result()
        rospy.loginfo("Yeni hedefe ulaşıldı.")

    def navigate_goals(self):
        """Verilen hedeflere sırasıyla git"""
        while self.current_goal_index < len(self.goals):
            goal = self.goals[self.current_goal_index]
            self.send_goal(goal)
            # Hedefe ulaşıldıktan sonra bir sonraki hedefe geç
            self.current_goal_index += 1

if __name__ == '__main__':
    rospy.init_node('goal_navigator')  # ROS düğümünü başlat
    navigator = GoalNavigator()  # GoalNavigator sınıfından bir nesne oluştur
    navigator.navigate_goals()  # Hedeflere sırasıyla git
