#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')
        self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.velocity_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose = Pose()
        self.goal_pose = Pose()
        self.goal_pose.x = 5.0  # Set your goal x-coordinate
        self.goal_pose.y = 5.0  # Set your goal y-coordinate
        self.tolerance = 0.01
        self.timer = self.create_timer(0.1, self.move_to_goal)

    def pose_callback(self, data):
        self.pose = data

    def euclidean_distance(self):
        return math.sqrt((self.goal_pose.x - self.pose.x)**2 + (self.goal_pose.y - self.pose.y)**2)

    def linear_velocity(self, constant=1.5):
        return constant * self.euclidean_distance()

    def steering_angle(self):
        return math.atan2(self.goal_pose.y - self.pose.y, self.goal_pose.x - self.pose.x)

    def angular_velocity(self, constant=6.0):
        return constant * (self.steering_angle() - self.pose.theta)

    def move_to_goal(self):
        if self.euclidean_distance() >= self.tolerance:
            vel_msg = Twist()

            # Linear velocity in the x-axis
            vel_msg.linear.x = self.linear_velocity()

            # Angular velocity in the z-axis
            vel_msg.angular.z = self.angular_velocity()

            # Publish the velocity message
            self.velocity_publisher.publish(vel_msg)
        else:
            # Stop the turtle when the goal is reached
            vel_msg = Twist()
            self.velocity_publisher.publish(vel_msg)
            self.get_logger().info('Goal reached!')
            self.timer.cancel()  # Stop the timer

def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
