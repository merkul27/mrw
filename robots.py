#!/usr/bin/env python3 
'''__class Robot__
Методы: Получение инфы от группы, перобразование в соар команды, передача инфы в соар, получение решение от соар и передача группе, вывод инфы о себе, инициализация
Получает от Группы расположение объектов, пробразует соар отправляет, возвращает решение группе
'''

class Robot:
    #rob_count = 0
    neibours = []
    
    def __init__(self, n, x, y, direct):
        self.num = n
        self.coord = (x, y) 
        self.direct = direct
        #Robot.rob_count += 1;
        
    def soar_command_create(self, neibours):
        # neibours := list with distances to other robots 0x, 0y (include itself or not?)
        soar_sentences = []
        big_dist = 10
        
        for nb in neibours:
            #print(nb)
            z = (nb[0] ** 2 + nb[1] ** 2) ** (0.5)
            if z < 0:
                print ("neibour distance error")
                break
            #print(z)
            if nb[0] > 0 and nb[1] > 0:     # ./
                if z <= big_dist:
                    soar_sentences.append("north-east nearby")
                elif z > big_dist:
                    soar_sentences.append("north-east away")
            elif nb[0] < 0 and nb[1] > 0:   # \.
                if z <= big_dist:
                    soar_sentences.append("north-west nearby")
                elif z > big_dist:
                    soar_sentences.append("north-west away")
            elif nb[0] < 0 and nb[1] < 0:   # /'
                if z <= big_dist:
                    soar_sentences.append("south-west nearby")
                elif z > big_dist:
                    soar_sentences.append("south-west away")
            elif nb[0] > 0 and nb[1] < 0:   # '\
                if z <= big_dist:
                    soar_sentences.append("south-east nearby")
                elif z > big_dist:
                    soar_sentences.append("south-east away")
            elif nb[0] == 0 and nb[1] > 0: # .|
                if nb[1] <= big_dist:
                    soar_sentences.append("north nearby")
                elif nb[1] > big_dist:
                    soar_sentences.append("north away")
            elif nb[0] == 0 and nb[1] < 0: # '|
                if abs(nb[1]) <= big_dist:
                    soar_sentences.append("south nearby")
                elif abs(nb[1]) > big_dist:
                    soar_sentences.append("south away")
            elif nb[0] > 0 and nb[1] == 0: # .-
                if nb[0] <= big_dist:
                    soar_sentences.append("east nearby")
                elif nb[0] > big_dist:
                    soar_sentences.append("east away")
            elif nb[0] < 0 and nb[1] == 0: # -.
                if abs(nb[0]) <= big_dist:
                    soar_sentences.append("west nearby")
                elif abs(nb[0]) > big_dist:
                    soar_sentences.append("west away")
            elif nb[0] == 0 and nb[1] == 0: # .
                soar_sentences.append("itself")
        
        return soar_sentences;
        
    def info_coord(self):         
        return self.coord
    
    def info_direct(self):        
        return self.direct
    
'''__Questions__
1. private and public atributes and methods?
2. soar sentences?
'''
    
'''__class Group__
класс Группа.
Атрибуты: Карта, Список роботов
Методы: Читает данные карты, окрестности-расположение предметов (других роботов) относительно робота, передача роботу инфы, получение решение от робота, принятие решения по передвижению
'''

class Group:
    #karta = []
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
            nb = (r.coord[0] - robot.coord[0], r.coord[1] - robot.coord[1])
            neibours.append(nb)
        return neibours
        
    '''def take_desicion (self):
        for r in robots:
            xy = r.info_coord()
            
        return 0'''
            
        
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
    for r in gr.robots:
        neighbourhood = gr.get_neighbourhood(r)
        print(neighbourhood)
        print(r.soar_command_create(neighbourhood))
    '''while True:
        group.take_desicion()'''
