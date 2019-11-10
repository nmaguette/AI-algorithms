# -*- coding: utf-8 -*-
# src https://blog.csdn.net/GarfieldEr007/article/details/50814664
import math

test_map = []

dictCellCost = {'w':100,'m':50,'f':10,'g':5,'r':1,'A':0,'B':1,'#':float('inf')}# a dictionary
FILEPATH = './boards/board-2-4.txt'
print("Search file : ",FILEPATH)

#########################################################
class Node_Elem:
    """
    type of openlist and closelist, definition of parent
    """
    def __init__(self, parent, x, y, dist):
        self.parent = parent
        self.x = x
        self.y = y
        self.dist = dist
        
class A_Star:
    """
    A* implementation
    """ 
    def __init__(self, s_x, s_y, e_x, e_y, w=60, h=30):
        self.s_x = s_x
        self.s_y = s_y
        self.e_x = e_x
        self.e_y = e_y
        
        self.width = w
        self.height = h
        
        self.open = []
        self.close = []
        self.path = []
        
    #find start point
    def find_path(self):
        #establish node
        p = Node_Elem(None, self.s_x, self.s_y, 0.0)
        while True:
            #extend min node of F
            self.extend_round(p)
            #if openlist is empty, there is no path, return
            if not self.open:
                return
            #get min F
            idx, p = self.get_best()
            #find path, make path, return
            if self.is_target(p):
                self.make_path(p)
                return
            #change this node to closelist, delet from openlist
            self.close.append(p)
            del self.open[idx]
            
    def make_path(self,p):
        #go back to starting point where parent == None
        while p:
            self.path.append((p.x, p.y))
            p = p.parent
        
    def is_target(self, i):
        return i.x == self.e_x and i.y == self.e_y
        
    def get_best(self):
        best = None
        bv = 1000000 #if map is huge, probably change this param
        bi = -1
        for idx, i in enumerate(self.open):
            value = self.get_dist(i)#get F value
            if value < bv:#if F is smaller, better than before
                best = i
                bv = value
                bi = idx
        return bi, best
        
    def get_dist(self, i):
        
        # F = G + H
        # G cost is what we had， H is the cost to end
        return i.dist + math.sqrt(
            (self.e_x-i.x)*(self.e_x-i.x)
            + (self.e_y-i.y)*(self.e_y-i.y))*1.2
        
        
    def extend_round(self, p):
##        #eight possibilities for next step's direction
##        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
##        ys = (-1,-1,-1,  0, 0,  1, 1, 1)
        #only considering 'up down left right'
        xs = (0, -1, 1, 0)
        ys = (-1, 0, 0, 1)
        for x, y in zip(xs, ys):
            new_x, new_y = x + p.x, y + p.y
            #no valid or not availble, ignore
            if not self.is_valid_coord(new_x, new_y):
                continue
            #new node
            node = Node_Elem(p, new_x, new_y,self.get_cell_cost(p)+p.dist+self.get_cost(
                        p.x, p.y, new_x, new_y))
            #ignore if new node in closelist
            if self.node_in_close(node):
                continue
            i = self.node_in_open(node)
            if i != -1:
                #if new node in openlist
                if self.open[i].dist > node.dist:
                    #if path now is better than the one before, use this one
                    self.open[i].parent = p
                    self.open[i].dist = node.dist
                continue
            self.open.append(node)

    def get_cell_cost(self,i):
        #-------for part 2---------#
        #---check target cell cost from dict---#
        letter = test_map[i.y][i.x]
        cellCost = dictCellCost.get(letter)
        return cellCost

    def get_cost(self, x1, y1, x2, y2):
        """
        up down left right->cost 1  diagonale -> cost 1.4
        cell costs r in dict
        """

        
        if x1 == x2 or y1 == y2:
            cost = 1.0
        cost = 1.4

        return cost

    def node_in_close(self, node):
        for i in self.close:
            if node.x == i.x and node.y == i.y:
                return True
        return False
        
    def node_in_open(self, node):
        for i, n in enumerate(self.open):
            if node.x == n.x and node.y == n.y:
                return i
        return -1
        
    def is_valid_coord(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return test_map[y][x] != '#'
    
    def get_searched(self):
        l = []
        for i in self.open:
            l.append((i.x, i.y))
        for i in self.close:
            l.append((i.x, i.y))
        return l
        
#########################################################
def print_test_map():
    for line in test_map:
        print (''.join(line))

def get_start_XY():
    return get_symbol_XY('A')
    
def get_end_XY():
    return get_symbol_XY('B')
    
def get_symbol_XY(s):
    for y, line in enumerate(test_map):
        try:
            x = line.index(s)
        except:
            continue
        else:
            break
    return x, y
        
#########################################################
def mark_path(l):
    COST = 0
    for i in l:
        letter = test_map[i[1]][i[0]]
        cellCost = dictCellCost.get(letter)
        COST += cellCost
    print ("Path cost is :", COST)
    mark_symbol(l, '*')
    
#def mark_searched(l):
    #mark_symbol(l, '.')
    
def mark_symbol(l, s):
    for x, y in l:
        test_map[y][x] = s
    
def mark_start_end(s_x, s_y, e_x, e_y):
    test_map[s_y][s_x] = 'A'
    test_map[e_y][e_x] = 'B'
    
def tm_to_test_map():
##    for line in tm:
    tm = open(FILEPATH,'r')
    for line in tm:
        line = line[:-1]    #delet all \n at end of each line
        test_map.append(list(line))
            
    #add borders around with '#'
    test_map.insert(0,'#'*(len(test_map[1])+2))# top border
    test_map.insert(len(test_map),'#'*(len(test_map[1])+2))#bottom border
    for i in range(1,len(test_map)-1):
        test_map[i].insert(0,'#')#left border
        test_map[i].insert(len(test_map[i]),'#')#right border
    #testmap is a list of list, every line in doc is a child-list
        
def find_path():
    s_x, s_y = get_start_XY()
    e_x, e_y = get_end_XY()
    a_star = A_Star(s_x, s_y, e_x, e_y)
    a_star.find_path()
    searched = a_star.get_searched()
    path = a_star.path
    #mark path
    mark_path(path)
    #mark starting and ending points
    mark_start_end(s_x, s_y, e_x, e_y)
    
if __name__ == "__main__":
    
    tm_to_test_map()
    find_path()
    print_test_map()
