#!/usr/bin/env python

import rospy
from std_srvs.srv import Trigger, TriggerResponse 
import socket
import sys


RESPONSE_OK  = 0x01
RESPONSE_ERROR = 0x02
RESPONSE_SIZE = 2

class SocketSAN:

    def __init__(self):
        
        # Init node
        rospy.init_node('san_socket_client', anonymous=False)

        # Get node name
        self.node_name = rospy.get_name()

        # Get ros params
        self.get_ros_params()

        # Create service to send a switch flag
        self.san_socket_flag = rospy.Service('san_socket/trigger_'+str(self.id), Trigger, self.callback_san_socket_trigger)

        # Connect to server running in san docker container
        self.san_server_connection()
    
    def get_ros_params(self):

        self.address = rospy.get_param(self.node_name + '/address','localhost')
        self.port = rospy.get_param(self.node_name + '/port',10000)
        self.id = rospy.get_param(self.node_name + '/id', 0)


    def san_server_connection(self):

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (self.address, self.port)
        print('Connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)


    def san_server_write(self, message):
        
        print("Sending: [" + message + "]")
        self.sock.sendall(message.encode('utf_8'))

    def san_server_read(self):
        
        status = RESPONSE_OK
        amount_received = 0
        
        last_time = rospy.Time.now().secs
        timeout = 5.0

        while amount_received < RESPONSE_SIZE:
            data = self.sock.recv(RESPONSE_SIZE)
            amount_received += len(data)
            print('Received from server: [{!r}]'.format(data))

            if (rospy.Time.now().secs - last_time > timeout):
                status = RESPONSE_ERROR
                break

        return status, data

    def trigger_san_socket(self):


        # Trigger san server socket
        self.san_server_write("True")

        # Get response
        status, data = self.san_server_read()


        if status == RESPONSE_OK:
            message = "Trigger sent to SAN docker successfully"
            success = True
        else:
            message = "Error sent trigger to SAN docker"
            success = False

        return message, success


    def callback_san_socket_trigger(self, req):

        result = TriggerResponse()
        result.message, result.success = self.trigger_san_socket()
        return result


    def run(self):

        rate = rospy.Rate(20)

        while not rospy.is_shutdown():

            rate.sleep()



if __name__ == '__main__':

    san = SocketSAN()

    try:
        san.run()

    except rospy.ROSInterruptException:
        pass