#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import random
from math import pi


class random_explore:
    def __init__(self):
        rospy.init_node('random_explore', anonymous=True)
        self.vel_cmd = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        rospy.Subscriber('/limo/scan', LaserScan, self.check_obstacle)
        rospy.sleep(1)
        rospy.on_shutdown(self.shutdown)
        self.if_obstacle = False
        
    def check_obstacle(self, data):
        # check if there is any obstacle in front of the robot
        
        # get the range of the laser scan
        ranges = data.ranges
        #get the area of the laser scan in front of the robot
        numbers = len(ranges)
        front_ranges = ranges[(numbers//2-20):(numbers//2+20)]
        print("Front ranges:", front_ranges[len(front_ranges)//2])
        # check if there is any obstacle in front of the robot
        for r in front_ranges:
            
            if r < 0.6:
                print("Obstacle detected!")
                self.if_obstacle = True
                rospy.sleep(0.2)
                return
            
        self.if_obstacle = False
        return
        
        
        
    
    def random_move(self,angle=0):
        # generate a random move
        move_forward = Twist()
        move_forward.linear.x = 0.3
        
        turn_around = Twist()
        # turn a random angle between -90 and 0 degrees
        turn_around.angular.z = angle 
        return move_forward, turn_around
    
    def main_loop(self):
        # main loop of the robot
        
        while not rospy.is_shutdown():
            angle = random.uniform(-pi/2, pi/2)
            #set the angle to -pi/2 or pi/2 if there is an obstacle in front of the robot
            angle = -pi/4 if angle < 0 else pi/4
            if self.if_obstacle:
                # if there is an obstacle in front of the robot, turn around
                while self.if_obstacle:
                    self.vel_cmd.publish(self.random_move(angle)[1])
                # rospy.sleep(0.1)
            else:
                # otherwise, move forward
                self.vel_cmd.publish(self.random_move(angle)[0])
            
            rospy.sleep(0.01)
        
                

        
                       
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.vel_cmd.publish(Twist())
        rospy.sleep(1)
    
if __name__ == '__main__':
    
    re = random_explore()
    re.main_loop()