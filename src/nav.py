#! /usr/bin/env python
import math
import rospy
from geometry_msgs.msg import Twist
from dynamixel_workbench_msgs.msg import DynamixelStateList
from std_msgs.msg import Bool

Ol=0.0
Or=0.0
Ob=0.0

N = {}
N["Left"]=0.0
N["Right"]=0.0
N["Rear"]=0.0

Dist_G,Theta_G=0,0

new_goal =False
theta_reached=False
offset_feedback=False

R=0.123
C=math.pi*0.1
cos30=math.sin((30*math.pi)/180)
reached = False
pub=None
pub1=None
flag_pub = None
theta_c = 0
dist = 0

def dist_correction():

	global N,new_goal,Dist_G,C,pub,pub1,linear_x,cos30,theta_reached,theta_c,dist,reached,flag_pub
	vel = Twist()
	if new_goal:
		rospy.loginfo(Dist_G)
		if Dist_G > 0:
			dr=C*N["Right"] + N["Right"]*0.043 #*cos30
			dl=C*N["Left"]+ N["Left"]*0.043 #*cos30
			dl=abs(dl)
			dist=(dr-dl)/2
			if ((Dist_G -abs(dist)) > 0.03):
				l= -0.05                 #FORWARDS
			#	rospy.loginfo("diff %f curr dist %f given dist %f ",Dist_G - dist,dist,Dist_G)
			else:
				new_goal=False
				reached =True
				flag_pub.publish(new_goal)
				l=0.0
		elif Dist_G<0:
			dl=C*N["Right"] + N["Right"]*0.043 #*cos30
			dr=C*N["Left"]+ N["Left"]*0.043 #*cos30
			dl=abs(dl)
			dist=(dr-dl)/2
			if ((abs(Dist_G) - abs(dist)) > 0.03):   #BACKWARDS
				l = 0.045
				rospy.loginfo("backwards")
			#	rospy.loginfo("diff %f curr dist %f given dist %f ",Dist_G - dist,dist,Dist_G)
			else:
				new_goal=False
				reached = True
				flag_pub.publish(new_goal)
				l=0.0
		else:
			l=0.0

	vel.linear.x=l
	pub.publish(vel)



def angular_correction():
	global N,C,new_goal,theta_reached,R,pub,cos30,Dist_G,theta_c
	vel = Twist()
	Ll=C*N["Left"]
	Lr=C*N["Right"]
	Lb=C*N["Rear"]
	avgl = (Lr+Ll+Lb)/3
	theta_c=math.degrees((avgl/R))

	dr=C*N["Right"]*cos30
	dl=C*N["Left"]*cos30
#	rospy.loginfo("dr  %f ",dr)
#	rospy.loginfo("dl  %f ",dl)
	dist=(dr-dl)/2

	if new_goal:
		if Theta_G > 0:
			if abs(Theta_G-abs(theta_c)) >1:
				angular= 0.25
			#	rospy.loginfo("angular_diff %f",abs(Theta_G-abs(theta_c)))
			#	rospy.loginfo("dist_diff %f",dist)
			else:
				angular = 0.0
				theta_reached= True

		else:
			if abs(Theta_G-theta_c) >1:
				angular= -0.25
#				rospy.loginfo("rev_diff %f",abs(Theta_G-theta_c))

			else:
				theta_reached= True
				angular=0.0

	vel.angular.z = angular
	pub.publish(vel)

def pose_callback(pos):
	global N,Ol,Or,Ob,offset_feedback

	for motor in pos.dynamixel_state:
		N[motor.name]=motor.present_position

	N["Left"] /=4096.0
	N["Right"]/=4096.0
	N["Rear"]/=4096.0
	if offset_feedback:
		Ol,Or,Ob=N["Left"],N["Right"],N["Rear"]
		offset_feedback=False
		rospy.loginfo("Values Offset Succesful")
	N["Left"]-=Ol
	N["Right"]-=Or
	N["Rear"]-=Ob
#	rospy.loginfo("N_Left: %f ",N["Left"])

def goal_callback(msg):
	global Theta_G,Dist_G,new_goal,offset_feedback,theta_reached
	global flag_pub
	Theta_G=msg.angular.z
	Dist_G = msg.linear.x
	new_goal=True
	flag_pub.publish(new_goal)
	offset_feedback=True
	theta_reached=False


def odom():
        global N,pub,new_goal,linear_x,pub1,dist,theta_c,dist,reached,flag_pub
	vel1=Twist()
	rospy.init_node('odometry')
	pub=rospy.Publisher("/dynamixel_workbench_base/cmd_vel",Twist,queue_size=1)
	rospy.Subscriber("/base/goal",Twist,goal_callback)
	pub1=rospy.Publisher("/base/current_pose",Twist,queue_size=1)
	flag_pub = rospy.Publisher("/goal/bool",Bool,queue_size=1)
	rospy.Subscriber("/dynamixel_workbench_base/dynamixel_state",DynamixelStateList,pose_callback)
	rate = rospy.Rate(20)

	while not rospy.is_shutdown():
		if new_goal:
			rospy.loginfo("Executing Goal")
			if not theta_reached:

				angular_correction()
			else:

				dist_correction()
		if reached:


			vel1.linear.x= -dist
			vel1.angular.z=theta_c
#			rospy.loginfo(vel1.linear.x)
#			rospy.loginfo(vel1.angular.z)
			pub1.publish(vel1)
#			flag_pub.publish(reached)
			print(reached)
			reached = False

		rate.sleep()


if __name__=="__main__":
	odom()


