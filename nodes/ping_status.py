#!/usr/bin/env python

'''
Run this as a ros node to check if a device is alive. Set the 
IP address and the topic name that you want to publish to. This
script uses the subprocess module to run the bash ping command
and publishes True or False if the ping is successful or not. 
Works in Python 2 or 3 on Ubuntu.
'''

import rospy
from std_msgs.msg import Bool
import subprocess
import os

class Alive(object):
    def __init__(self):
        self.pub_topic = 'ip_status'
        self.pub_type = Bool
        self.pub = rospy.Publisher(self.pub_topic, self.pub_type, queue_size=1, latch=False)
        self.ip = '127.0.0.1' #IP address to check if alive

    def update(self):
        pub_msg = self.ping(self.ip)
        self.pub.publish(pub_msg)

    def ping(self, ip):
        command = ['ping','-c','1',ip]
        with open(os.devnull, 'wb') as dnull:
            return subprocess.call(command, stdout=dnull, stderr=dnull) == 0
        
def main():
    try:
        rospy.init_node('ping_status', anonymous=False)
        alive_obj = Alive()
        rrate = rospy.Rate(0.2) #0.2 Hz = 5 sec update rate
        while not rospy.is_shutdown():
            alive_obj.update()
            rrate.sleep()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
	main()
