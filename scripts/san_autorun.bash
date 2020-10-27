#!/bin/bash

export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost

source ~/catkin_ws/devel/setup.bash

echo "SAN OPIL AUTORUN"

screen -S san -d -m roslaunch san_socket multiple_client.launch;
