import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/wade/ros2_ws/src/python_parameters/install/python_parameters'
