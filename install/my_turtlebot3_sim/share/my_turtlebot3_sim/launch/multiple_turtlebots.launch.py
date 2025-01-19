from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import os

def generate_launch_description():
    # Define positions for each robot
    robots = [
        {'namespace': 'tb3_1', 'x': 0.0, 'y': 0.0, 'z': 0.01},
        {'namespace': 'tb3_2', 'x': 2.0, 'y': 0.0, 'z': 0.01},
    ]

    # Path to the TurtleBot 3 Gazebo world launch file
    pkg_share = os.path.join(os.getenv('AMENT_PREFIX_PATH'), 'share', 'turtlebot3_gazebo')
    launch_file_path = os.path.join(pkg_share, 'launch', 'empty_world.launch.py')

    launch_descriptions = []

    for robot in robots:
        launch_descriptions.append(
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(launch_file_path),
                launch_arguments={
                    'namespace': robot['namespace'],
                    'x': str(robot['x']),
                    'y': str(robot['y']),
                    'z': str(robot['z']),
                }.items(),
            )
        )

    return LaunchDescription(launch_descriptions)