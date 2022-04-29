#!/usr/bin/env python3 

import sys
# load Soar library
sys.path.append('/opt/Soar/out')
import Python_sml_ClientInterface as sml

# function to print Soar output
def cb_print_soar_message(mid, user_data, agent, message):
    print(message.strip() + '\n')


'''
__class Robot__
Methods: __init__; soar_command_create(take neibours and single robot, make soar_sentences); info_coord; info_direct; make_decision(take soar_sentences work with soar and return soar desicion); robot_movement(take soar decision and move single robot)
'''


class Robot:
    #rob_count = 0
    neibours = []
    
    def __init__(self, n, x, y, direct):
        self.num = n
        self.coord = (x, y) 
        self.direct = direct # в градусах!
        #Robot.rob_count += 1;
        
    def soar_command_create(self, neibours):
        # neibours := list with distances to other robots 0x, 0y (include itself or not?)
        soar_sentences = []
        big_dist = 10
        
        for nb in neibours:
            #print(nb)
            d = self.direct
            z = (nb[0] ** 2 + nb[1] ** 2) ** (0.5)
            nd =    #direct where is neibour 
            if z < 0:
                print ("neibour distance error")
                break
            
            
        return soar_sentences;
        
    def info_coord(self):         
        return self.coord
    
    def info_direct(self):        
        return self.direct
    
    def make_decision():
        # create processing kernel
        kernel = sml.Kernel.CreateKernelInCurrentThread()
        agent = kernel.CreateAgent("agent")
        
        # add method to print debug messages from Soar
        agent.RegisterForPrintEvent(sml.smlEVENT_PRINT,
                            cb_print_soar_message,
                            None)
        agent.ExecuteCommandLine("watch 5")
        agent.ExecuteCommandLine("source robots.soar")
        agent.RunSelf(1)
        input_link = agent.GetInputLink()
        #LOOP with soar_command_create
        agent.RunSelf(2)
        output_link = agent.GetOutputLink()
        if output_link != None:
            try:
                result_output_wme = output_link.FindByAttribute("target", 0)
                target = result_output_wme.GetValueAsString()
            except AttributeError:
                print("error") #error
        else:
            print("error")
        targets.append(target)
        kernel.DestroyAgent(agent)
        kernel.Shutdown()
        
    def robot_movement()
    
'''
__class Group__
Methods: get_neighbourhood(create neibours with coordinates in relation to one robot and direct); movement(take decisions from robots and take one move)
'''

class Group:
    robots = []
    
    #def __init__(self):
        #robots = []
    #def neibors(self, robot):
        #find all robots 
        
    '''def get_info(self):
        return robots'''
    
    def get_neighbourhood(self, robot):
        neibours = []
        for r in self.robots:
            nb = (r.coord[0] - robot.coord[0], r.coord[1] - robot.coord[1], r.direct)
            neibours.append(nb)
        return neibours
    
    def movement(self) #take decisions from robots and take one move
            
        
'''Запуск
Вбиваются данные роботов: забиваются в группу и в карту!!!
Запускаем с картой группу, которая по циклу опрашивает роботов и получает 
# решения от каждого это один цикл
# Цикл заканчивается при достижении условий
'''
if __name__ == "__main__":      #use or not to use?
    n = 0
    gr = Group()
    while True: 
        n += 1
        #line = input("enter robot's coordinates and direction or Enter to finish: ")
        line = input()
        if not line:
            break
        data = line.split()
        gr.robots.append(Robot(n, int(data[0]), int(data[1]), data[2]))
        
    
    for r in gr.robots:
        print(r.info_coord(), r.info_direct())
    #for r in gr.robots:
        neighbourhood = gr.get_neighbourhood(r)
        print(neighbourhood)
        print(r.soar_command_create(neighbourhood))
    '''while True:
        group.take_desicion()'''
