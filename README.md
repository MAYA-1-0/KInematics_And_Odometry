# Kinematics_And_Odometry

#####  This repository contains kinematic and Odometry modelling of MAYA

##### Robot wheel configuration

![config](https://github.com/MAYA-1-0/KInematics_And_Odometry/blob/main/images/Screenshot%20from%202022-02-26%2021-26-41.png)

This system used a three wheeled omnidirectional robot which is at 120 degrees from each other mounted on a triangular platform. Two wheels are considered as Front left and Front Right while the remaining wheel is considered as Rear wheel.

The forward motion of the robot is achieved by rotating Front left and Front right wheels in opposite directions to each other while the rear wheel is not actuated actively, the rollers present in the rear omnidirectional wheels actuates the robot efficiently. The Angular motion of the robot is achieved by rotating all the three wheels in the same direction.

The platform origin is located at its geometric median and all kinematic calculations are done based on this assumption.

Let ‘R’ be the radius of the three omnidirectional wheels, ‘r’ be the wheel separation i.e the distance from platform’s centre to each wheel. Number of rotations is taken as feedback from each wheel’s encoder.

Dynamixel MX106 motors are employed for the work, Dynamixel motors offer excellent features like precise position control, PID correction (less backlash), 360-degree position control, and fast communication.
Several rotations from each wheel are separately subscribed over a ROS topic and are denoted as Nr, Nl, Nb in the calculations which are divided by a factor of 4096 which is the total number of steps in the dynamixel motor.

This project was built and Deployed on 2 Nvidia Jetson nano devices, so for communication between various sensors and wheels connected to both devices ( more information can be found in [Humanoid's Architecture Repository](https://github.com/MAYA-1-0/MAYA1.0_Architecture)
For running a common master over all system, follow the below steps
1. Run rosmaster in host computer
```
rosmaster
```

2. Run ```ifconfig``` to get the ip address of any system
3. Run the following commands in each terminal (or preferably add in bashrc Script) to create a remote master.
    ```
        export ROS_MASTER_URI=http://<HOST IP>:11311
    ```
    
    ```
        export ROS_IP=<remote/current system's IP>
    ```
    
    ```
        export ROS_HOSTNAME=<remote/current system's IP>
    ```

### Usage and Requirements

1. Clone this repository and put it under a ROS package named <odometry>
2. For running Dynamizel motors by publishing commands we will need dynamixel workbench messages, This can be cloned to the same ROS Workspace
```
  git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench-msgs.git
```
3. Pull docker image by typing the below in a terminal (Type trl+ Alt + T )
```
  docker pull mayakle/maya_wheels:3_wheeled
```
4. Open a terminal and type ,
```
  docker run -it --net=host 
```
  This should create a docker, inside the docker 
  NOTE: Before doing the following it is assumed thst the dynamixel motors have IDs set and same is mentioned in the yaml file which is inside docker (e.g : home/catkin_ws/src/dynamixel_workbench/dynamixel_workbench_controllers/config/joints.yaml), refer [robotics emanual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/) to do the same.
   
  ```
      source home/catkin_ws/devel/setup.bash
  ```
  ```
      roslaunch dynamixel_workbench_controllers dynamixel_workbench_controllers.launch
  ```
  If all the motor have their IDs set and are detected, this will launch all the controllers (Topics and Services) in the dynamixel workbench,
  Running ``` rostopic list``` and ```rosservice list``` will dislay all the topics and services from dynamixel workbench. 
5.  To switch on the Torque, which can be done by calling a service
  Open a terminal and type,
  ```
      rosservice call /dynamixel_workbench_base/dynamixel_controllers/dynamixel_command "Torque : True"
  ```
  
6. Open a terminal and run,
```
    rosrun odometry nav.py
```
Topic named maya/base/goal will start running, to which linear distance and theta can be published in order to move the robot 
  
  
7. To control the robot through Keyboard, after running above script, run
```
    rosrun odometry teleop.py
```


















