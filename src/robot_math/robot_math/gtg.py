import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import sys
import math

class Turtle_GTG(Node):  # Creating a T_gtg Node.

    # Initialize T_GTG Class, runs every time on calling.
    def __init__(self):
        # Calls the constructor of the parent class 
        # ( Inherit from Node )
        super().__init__("Go_to_Goal_Node") # Creating Name of node
        
        # Creates a publisher for sending velocity commands to the /turtle1/cmd_vel topic. ( Message of type TWIST, queue size = 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Creates a subscription to the /turtle1/pose topic, which provides the turtles current position and orientation.
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        
        # Timer that calls go_to_goal method every 0.1 seconds
        self.timer = self.create_timer(0.1, self.go_to_goal)
        
        self.pose = Pose()


# Convention of recievind position
    def pose_callback(self, data):
        self.pose = data


    def go_to_goal(self):
        goal = Pose()
        goal.x = float(sys.argv[1])
        goal.y = float(sys.argv[2])
        goal.theta = float(sys.argv[3])

        new_vel = Twist()

        # Ecludian Distance
        distance_to_goal = math.sqrt( (goal.x - self.pose.x)**2  + (goal.y - self.pose.y)**2 )
        # Angle to Goal
        angle_to_goal = math.atan2(goal.y - self.pose.y , goal.x - self.pose.x)

        distance_tolerance = 0.1  # Distance Error
        angle_tolerance = 0.01   # Angle Error

        # Difference between desired and current orientation.
        angle_error = angle_to_goal - self.pose.theta


        ## Firstly get the angle correct
        if abs(angle_error) > angle_tolerance:
            new_vel.angular.z = angle_error
        
        ## Then 
        else :
            if( distance_to_goal ) >= distance_tolerance:
                new_vel.linear.x = distance_to_goal
            else :
                new_vel.linear.x= 0.0
                self.get_logger().info("Goal Reached ")
                quit()

        self.cmd_vel_pub.publish(new_vel)

def main(args=None):         # ALLOWS Function to take a list of command-line arguments.
                             # If no argument provided, default to None.

# Initialize the Ros2 class, for performing ros-related-tasks.

    rclpy.init(args=args)    # Passes any command line arguments
    minimal_publisher = Turtle_GTG()
    
# Keeps the node running
    rclpy.spin(minimal_publisher)
    
# Shutdown when node stops.
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()