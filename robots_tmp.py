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
класс Робот 
номер от счетчика ввода, координаты и направление из файла ввода, валентности начальные значения None
'''
class Robot:
    def __init__(self, n, x, y, direct):
        self.num = n
        self.status = 0 #флаг - стоит в решетке или нет
        coord = (x, y)
        self.coord = list(coord)
        self.direct = direct #??? look gazebo относительно одной СО
        self.name = "robot" + str(n)
        #for rectangular lattice formation
        self.valence = [None] * 3 
        # create processing kernel and agent
        self.kernel = sml.Kernel.CreateKernelInCurrentThread()
        self.agent = self.kernel.CreateAgent("agent")
        
        # add method to print debug messages from Soar
        if self.num == 1:
            self.agent.RegisterForPrintEvent(sml.smlEVENT_PRINT,
                                cb_print_soar_message,
                                None)
        
        self.agent.ExecuteCommandLine("watch 5")
        self.agent.ExecuteCommandLine("source lattice.soar")
        self.agent.RunSelf(1)
        
    def soar_command_create(self, neibours):
        # neibours := list with distances to other robots 0x, 0y (including itself)
        soar_sentences = []
        big_dist = 3
        d = int(self.direct)
            
        for nb in neibours:
            z = (nb[0] ** 2 + nb[1] ** 2) ** (0.5)
            x = nb[0] * math.cos(math.radians(d)) - nb[1] * math.sin(math.radians(d))
            y = nb[0] * math.sin(math.radians(d)) + nb[1] * math.cos(math.radians(d)) 
            #coordinates where is neibour относит взгляда робота
            
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
            direct = w[0]
            dist = w[1]
            i += 1
            r_link = self.agent.CreateStringWME(input_link,
                                               w[1], 
                                               'r' + str(i))
            
            robot_link = self.agent.CreateIdWME(input_link,
                                               'near')
            place1_link = = self.agent.CreateStringWME(robot_link,
                                               'place', 
                                               'left')
            place2_link = = self.agent.CreateStringWME(robot_link,
                                               'place', 
                                               'right')
            #создание дерева пример
            
            #TODO valence_link
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
                print("error") 
        else:
            #target = ""
            print("error")
        #targets.append(target)
        print(target) #TODO target теперь не только номер робота но и положение относительно него
        #kernel.Shutdown()
        return target
        #move one robot one step
  
    def make_decision_alter(self, soar_sentences):
        #soar_sentences уже только с лидерами
        print("working with robot{}".format(self.num))
        input_link = self.agent.GetInputLink()
        robot_links = []
        i = 0
        for s in soar_sentences:
            if s == 'itself' or s == 'not valid':
                i += 1
                continue
            w = s.split
    
    def move(self,target): #target в виде (x, y)
        print("in move {}".format(target))
        print("origin direct {}".format(self.direct))
        self.direct = math.degrees(math.atan2(target[1],target[0]))
        print("new direct {}".format(self.direct))
        self.coord[0] += target[0]/2
        self.coord[1] += target[1]/2
        

'''
__class Group__
Methods: get_neighbourhood(create neibours with coordinates in relation to one robot and direct); process(take decisions from robots and create moves); movement(move everybody same time or single robot, change coordinates or map???)
list_valence (вакантные места транслируются для всех роботов)
'''

class Group(list):  #добавление валентностей
    robots = []
    places = []
    
    #def __init__(self):
        #robots = []
    #k=1 -- left, k=2 -- right, k=3 -- back
    def get_valences(self, robot):
        for r in self.robots:
            k = 0
            for v in r.valence:
                k += 1
                if v == 'place':
                    places.append([r.num, k])
    
    #получать положение только роботов с местами ПОТОМ
    #def get_lider_soar_command(self, robot):
        
    
    def get_neighbourhood(self, robot): 
        neibours = []
        for r in self.robots:
            nb = (r.coord[0] - robot.coord[0], r.coord[1] - robot.coord[1]) #(x,y) -> (x~,y~)
            #print("in get_nei {}".format(nb))
            
            neibour = (nb[0], nb[1]) #(x~,y~,z)
            
            neibours.append(neibour)
        return neibours
    
    #не было данных о не лидерах или данные о лидерах отличаличь здесь или в spec_soar_command_create
    def get_neighbourhood_alter(self, robot):
    
    #не было данных о не лидерах или данные о лидерах отличаличь здесь или в get_neighbourhood_alter
    def spec_soar_command_create(self, neibours):
    
    def process(self): #take decisions from robots and take one desicions
        targets = []
        for r in self.robots:
            targets.append(r.make_decision(r.soar_command_create(self.get_neighbourhood(r))))
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
            
        
'''Запуск
Вбиваются данные роботов: из файла input_robot формат: 2 2 90 - координаты и абсолютное направление в градусах
Запускаем группу, которая по циклу опрашивает роботов и получает решения от каждого это один цикл
Цикл заканчивается при достижении условий 
'''
if __name__ == "__main__":
    n = 0
    gr = Group()
    
    while True: 
        n += 1
        line = input()
        if not line:
            print("None input")
            break
        data = line.split()
        r = Robot(n, int(data[0]), int(data[1]), int(data[2]))
        gr.robots.append(r)
        if r.num == 1:
            r.valence = ['place'] * 3
            r.status = 1
        print("create {}".format(r.name))
    
    while True:
        res = gr.process()
        print(res)
        if (gr.movement(res) == 1):
            print("ALL STAY")
            break
        for r in gr.robots:
            print(r.coord)

