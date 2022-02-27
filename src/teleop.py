#! /usr/bin/env python
#import keyboard
import rospy
from geometry_msgs.msg import Twist

def teleop():

        rospy.init_node('manual_control')
        print("8 - forward\n 4 -left\n 6 - right\n 5-stop\n")
#       w,a,s,d = 1,2,3,4 
        pub=rospy.Publisher("/base/goal",Twist,queue_size=1)
        vel=Twist()
#       command = 0
        while True:
                command = int(input())          
                if  command == 8:        #forward
                        vel.angular.z = 0.0
                        vel.linear.x = 0.2
                        pub.publish(vel)
                        rospy.sleep(1)
                elif command == 5:  #stop
                        vel.angular.z = 0.0
                        vel.linear.x = 0.0
                        pub.publish(vel)
                        rospy.sleep(1)
                elif command == 4:   #left
                        vel.angular.z = -10
                        vel.linear.x = 0.0
                        pub.publish(vel)
                        rospy.sleep(1)
                elif command == 6:  #right
                        vel.angular.z = 10
                        vel.linear.x = 0.0
                        pub.publish(vel)
                        rospy.sleep(1)
                else:
                        vel.angular.z = 0.0
                        vel.linear.x = 0.0
                        pub.publish(vel)
                        rospy.sleep(1)
                        print("enter 8,4,6,5")



if __name__ == "__main__":
        teleop()

