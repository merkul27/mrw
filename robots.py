#!/usr/bin/env python3 
import math
import sys
# load Soar library
sys.path.append('/opt/Soar/out')
import Python_sml_ClientInterface as sml


# function to print Soar output
def cb_print_soar_message(mid, user_data, agent, message):
    print(message.strip() + '\n')

'''
__class Robot__
Methods: __init__; soar_command_create(take neibours(Group) and single robot, make soar_sentences); info_coord; info_direct; make_decision(take soar_sentences work with soar and return soar target); robot_move(take decision(Group.movement) and move robot)
'''


class Robot:
    #rob_count = 0
    #neibours = []
    
    def __init__(self, n, x, y, direct):
        self.num = n
        self.coord = (x, y) 
        self.direct = direct # в градусах! [0,360) полярные координаты??? [x,y] --> [r,fi] x=r*cos(fi), y=r*sin(fi) 
        #Robot.rob_count += 1;
        # create processing kernel and agent
        self.kernel = sml.Kernel.CreateKernelInCurrentThread()
        self.agent = self.kernel.CreateAgent("agent")
        
        # add method to print debug messages from Soar
        self.agent.RegisterForPrintEvent(sml.smlEVENT_PRINT,
                            cb_print_soar_message,
                            None)
        self.agent.ExecuteCommandLine("watch 5")
        self.agent.ExecuteCommandLine("source robots.soar")
        self.agent.RunSelf(1)
        
    def soar_command_create(self, neibours):
        # neibours := list with distances to other robots 0x, 0y (including itself)
        soar_sentences = []
        big_dist = 10
        
        for nb in neibours:
            x = nb[0]
            y = nb[1]
            z = nb[2]
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
        self.agent.RunSelf(2)
        for r in robot_links:
            self.agent.DestroyWME(r)
        target = "None"
        output_link = self.agent.GetOutputLink()
        
        if output_link != None:
            try:
                result_output_wme = output_link.FindByAttribute("target", 0)
                target = result_output_wme.GetValueAsString()
            except AttributeError:
                #target = "None"
                print("error") 
        else:
            #target = ""
            print("error")
        #targets.append(target)
        print(target)
        #kernel.Shutdown()
        return target
        #move one robot one step
        
    def move(self,target): #target в виде ri вытаскиваем номер робота смотрим его положение в соседях и двигаемся в направлении (с поворотом или без?). пока по тупому просто на фиксированный шаг.
        
  
    
'''
__class Group__
Methods: get_neighbourhood(create neibours with coordinates in relation to one robot and direct); process(take decisions from robots and create moves); movement(move everybody same time or single robot, change coordinates or map???)
'''

class Group(list):  #добавление наследования? extend append
    robots = []
    
    #def __init__(self):
        #robots = []
    #def neibors(self, robot):
        #find all robots 
        
    '''def get_info(self):
        return robots
        
        сделать наследование от map и применять ко всем роботам функцию переводав сферические координаты
        '''
        
    
    def get_neighbourhood(self, robot): 
        neibours = []
        for r in self.robots:
            nb = (r.coord[0] - robot.coord[0], r.coord[1] - robot.coord[1])
        #print(nb)
            d = int(r.direct)
            z = (nb[0] ** 2 + nb[1] ** 2) ** (0.5)
            x = nb[0] * math.cos(math.radians(d)) - nb[1] * math.sin(math.radians(d))
            y = nb[0] * math.sin(math.radians(d)) + nb[1] * math.cos(math.radians(d))
            #coordinates where is neibour относит взгляда робота матрица перехода турупупум
            neibour = (x, y, z)
            neibours.append(neibour)
        return neibours
    
    def process(self): #take decisions from robots and take one desicions
        targets = []
        for r in self.robots:
            targets.append(r.make_decision(r.soar_command_create(self.get_neighbourhood(r))))
        return targets
        #HOW compare/check/make decision? changing targets or from targets make other array - 'moves'
        #change in future. in present soar_command first word -> moves
        #self.movement(moves)
        #return moves    
    
    def movement(self, targets): #move everybody same time or single robot, change coordinates or map??? 
        for r in self.robots:
            #neibours = self.get_neighbourhood(r)
            r.move(targets[r.num - 1])
            #check in future. in present ==. create move = (dx,dy)
            
            
        
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
        gr.robots.append(Robot(n, int(data[0]), int(data[1]), int(data[2])))
        print("create r{}".format(n))
    print(gr.process())
    
    '''for r in gr.robots:
        print(r.info_coord(), r.info_direct())
    #for r in gr.robots:
        neighbourhood = gr.get_neighbourhood(r)
        print(neighbourhood)
        print(r.soar_command_create(neighbourhood))
        while True:
        group.take_desicion()'''
