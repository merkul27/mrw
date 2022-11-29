#!/usr/bin/env python3

import math
import sys
# load Soar library
sys.path.append('/opt/Soar/out')
import Python_sml_ClientInterface as sml
import random
import rospy

from geometry_msgs.msg import PoseStamped
from gazebo_msgs.msg import ModelStates 


# function to print Soar output
def cb_print_soar_message(mid, user_data, agent, message):
    print(message.strip() + '\n')


class Robot:
    def __init__(self, n, x, y, direct):
        self.num = n
        coord = (x, y)
        self.coord = list(coord)
        self.direct = direct
        self.name = "robot" + str(n)
        # create processing kernel and agent
        self.kernel = sml.Kernel.CreateKernelInCurrentThread()
        self.agent = self.kernel.CreateAgent("agent")
        self.agent.ExecuteCommandLine("watch 5")
        soar_config_file = rospy.get_param('~soar_config_file')
        self.agent.ExecuteCommandLine("source " + soar_config_file)

        # add method to print debug messages from Soar
        if self.num == 1:
            self.agent.RegisterForPrintEvent(sml.smlEVENT_PRINT,
                                cb_print_soar_message,
                                None)
        self.agent.RunSelf(1)

        output = '/' + self.name + '/move_base_simple/goal'
        self.output_pub = rospy.Publisher(output, PoseStamped, queue_size=1)
        self.input_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.cb_robot_pos)
         
        
        
        
    def soar_command_create(self, neibours):
        # neibours := list with distances to other robots 0x, 0y (including itself)
        soar_sentences = []
        big_dist = 1
        d = int(self.direct)
            
        for nb in neibours:
            z = (nb[0] ** 2 + nb[1] ** 2) ** (0.5)
            x = nb[0] * math.cos(math.radians(d)) - nb[1] * math.sin(math.radians(d))
            y = nb[0] * math.sin(math.radians(d)) + nb[1] * math.cos(math.radians(d)) 
            #coordinates where is neibour относит взгляда робота матрица перехода турупупум
             
            if x > 0 and y > 0:     # ./
                if z <= big_dist:
                    soar_sentences.append("front-right nearby")
                elif z > big_dist:
                    soar_sentences.append("front-right away")
            elif x < 0 and y > 0:   # \.
                if z <= big_dist:
                    soar_sentences.append("front-left nearby")
                elif z > big_dist:
                    soar_sentences.append("front-left away")
            elif x < 0 and y < 0:   # /'
                if z <= big_dist:
                    soar_sentences.append("back-left nearby")
                elif z > big_dist:
                    soar_sentences.append("back-left away")
            elif x > 0 and y < 0:   # '\
                if z <= big_dist:
                    soar_sentences.append("back-right nearby")
                elif z > big_dist:
                    soar_sentences.append("back-right away")
            elif x == 0 and y > 0: # .|
                if y <= big_dist:
                    soar_sentences.append("front nearby")
                elif y > big_dist:
                    soar_sentences.append("front away")
            elif x == 0 and y < 0: # '|
                if abs(y) <= big_dist:
                    soar_sentences.append("back nearby")
                elif abs(y) > big_dist:
                    soar_sentences.append("back away")
            elif x > 0 and y == 0: # .-
                if x <= big_dist:
                    soar_sentences.append("right nearby")
                elif x > big_dist:
                    soar_sentences.append("right away")
            elif x < 0 and y == 0: # -.
                if abs(x) <= big_dist:
                    soar_sentences.append("left nearby")
                elif abs(x) > big_dist:
                    soar_sentences.append("left away")
            elif x == 0 and y == 0: # .
                soar_sentences.append("itself")
        print(soar_sentences)
        return soar_sentences;
    
    def make_decision(self, soar_sentences):
        print("working with r{}".format(self.num))
        input_link = self.agent.GetInputLink()
        #LOOP with soar_command_create
        i = 0
        #print(soar_sentences)
        robot_links = []
        for s in soar_sentences:
            if s == 'itself':
                i += 1
                continue
            w = s.split()
            if len(w) < 2:
                print('wrong status "{}"'.format(s))
                continue
            word = w[1]
            i += 1
            r_link = self.agent.CreateStringWME(input_link,
                                               word, 
                                               'r' + str(i))
            robot_links.append(r_link)
        self.agent.RunSelf(1)
        for r in robot_links:
            self.agent.DestroyWME(r)
        self.agent.RunSelf(1)
        target = "None"
        output_link = self.agent.GetOutputLink()
        
        if output_link != None:
            try:
                result_output_wme = output_link.FindByAttribute("target", 0)
                target = result_output_wme.GetValueAsString()
            except AttributeError:
                #target = "None"
                print("attribute_error") 
        else:
            #target = ""
            print("output_link error")
        #targets.append(target)
        print(target)
        #kernel.Shutdown()
        return target
        #move one robot one step
        
    # now use movebase! TODO in future change to pid controller?
    def move(self,target): #target в виде (x, y)
        print("in move {}".format(target))
        print("origin direct {}".format(self.direct))
        self.direct = math.degrees(math.atan2(target[1],target[0]))
        print("new direct {}".format(self.direct))
        # create output message
        gx = self.coord[0] + target[0]/4
        gy = self.coord[1] + target[1]/4
        output_msg = PoseStamped()
        output_msg.header.frame_id = 'map'
        output_msg.pose.position.x = gx
        output_msg.pose.position.y = gy
        output_msg.pose.orientation.z = math.sin(0.5 * self.direct) # TODO self.direct change to target_ori
        output_msg.pose.orientation.w = math.cos(0.5 * self.direct)
        # send message
        self.output_pub.publish(output_msg)
        '''while True:
            rospy.sleep(1)
            #rospy.loginfo('Current pos: {:.2f} {:.2f} {:.2f}'.format(robot_x, robot_y, robot_ori))
            if abs(gx - self.coord[0]) < 0.3 and abs(gy - self.coord[1]) < 0.3:
                rospy.loginfo('Leader have reached goal: {:.2f} {:.2f} {:.2f}'.format(robot_x, robot_y, robot_ori))
                break'''
        
        
    # function to get robot's coordinates and orientation
    # where?
    def cb_robot_pos(self, msg):
        # where was 'test_robot' in example with move_node.py??? is it 'robotn' now?? 
        # get index
        # rospy.logerr('Names: {} {}'.format(self.name, msg.name))
        if self.name not in msg.name:
            return
        ind = msg.name.index(self.name)
        # read data
        x = msg.pose[ind].position.x
        y = msg.pose[ind].position.y
        self.direct = 2*math.atan2(msg.pose[ind].orientation.z,
                                msg.pose[ind].orientation.w)  
        coord = (x, y)
        self.coord = list(coord)
        
class Group():
    
    def __init__(self):
        self.robots = []
        
    def get_neighbourhood(self, robot): 
        neibours = []
        for r in self.robots:
            if r.coord[0] is None or robot.coord[0] is None:
                continue
            nb = (r.coord[0] - robot.coord[0], r.coord[1] - robot.coord[1]) #(x,y) -> (x~,y~)
            #print("in get_nei {}".format(nb))
            
            neibour = (nb[0], nb[1]) #(x~,y~,z)
            #print("in get_neibourhood {}".format(neibour))
            neibours.append(neibour)
        return neibours
    
    def process(self): #take decisions from robots and give one desicions
        targets = []
        print("THINKING PROCESS")
        for r in self.robots:
            if r.direct is None:
                continue
            print("for robot number: {}".format(r.num))
            #targets.append(r.make_decision(r.soar_command_create(self.get_neighbourhood(r))))
            neibours = self.get_neighbourhood(r)
            print("neighbourhood is: {}".format(neibours))
            soar_commands = r.soar_command_create(neibours)
            print("its soar sentences look like: {}".format(soar_commands))
            target = r.make_decision(soar_commands)
            print("and soar target is: {}".format(target))
            targets.append(target)
        return targets
    
    def movement(self, targets):  
        print('Targets: ', targets)
        s = 0
        for r in self.robots:
            print("count of stays: {}".format(s))
            #neibours = self.get_neighbourhood(r)
            if (len(targets[r.num-1]) > 2):
                s += 1
                continue
            new_target = targets[r.num-1]
            #print("in movement {}".format(new_target))
            if new_target != 'None':
                k = int(new_target[1])
                #print("in movement {}".format(k))
                neiborhood = self.get_neighbourhood(r)
                t = neiborhood[k-1]
                r.move(t)
        if (s == 3):
            for r in self.robots:
                print("coordinates {}".format(r.coord))
            return 1
            #check in future. in present ==. create move = (dx,dy)
        return 0
    
    def wait(self):
        for r in self.robots:
            if r.direct is None:
                return True
            else:
                return False

# function to print Soar output
def cb_print_soar_message(mid, user_data, agent, message):
    print(message.strip() + '\n')


if __name__ == '__main__':
    # connect to roscore
    rospy.init_node('soar_gazebo')

    n = 0
    gr = Group()
    # take robot's data from gazebo and send in Group 
    for n in range(3):
        n += 1
        #without data TODO 
        gr.robots.append(Robot(n, None, None, None))
        print("create robot{}".format(n))
    
    while gr.wait():
        print("WAIT")
        rospy.sleep(3.)
    
    
    while True:
        #k += 1
        rospy.sleep(1.)
        res = gr.process()
        print (res)
        if (gr.movement(res) == 1):
            print("ALL STAY")
            break
        rospy.sleep(10.)
        
        
        #print robots' coord after movement
        for r in gr.robots:
            print(r.coord)
         
        # when leader reach the goal he stop and wait like this??
        '''
        while True:
            rospy.sleep(1)
            #rospy.loginfo('Current pos: {:.2f} {:.2f} {:.2f}'.format(robot_x, robot_y, robot_ori))
            if abs(gx - robot_x) < 0.3 and abs(gy - robot_y) < 0.3:
                rospy.loginfo('Leader've reached goal: {:.2f} {:.2f} {:.2f}'.format(robot_x, robot_y, robot_ori))
                break
        '''
