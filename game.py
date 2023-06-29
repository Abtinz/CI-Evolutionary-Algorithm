import copy
import os
import random
import time

import numpy as np
from matplotlib import pyplot as plt

class Game:
    def __init__(self, levels):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps
         # store current levels index for processing them in order...
        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0
    
    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def read_level_from_file(name):
        level = open(name, 'r').readline()
        return level, len(level)


    def population(gens_count, chromosome_count):
        # chromosomes = [[random.randint(0,2) for i in range(len)] for j in range(200)]
        chromosome = [[np.random.choice(np.arange(0, 3), p=[0.5, 0.4, 0.1]) for i in range(gens_count)] for j in range(chromosome_count)]
        return chromosome
    
    def get_score(self, actions):
        # Get an action sequence and determine the steps taken/score
        # Return a tuple, the first one indicates if these actions result in victory
        # and the second one shows the steps taken

        current_level = self.levels[self.current_level_index]
        alive_steps = 0
        score = 0.0
        mushroom_point = 0
        wining = True
        jump_before_end = False
        not_a_good_jump = 0
        killed_gumpas_count = 0

        for i in range(self.current_level_len):
            current_step = current_level[i]
            next_step, second_next_step =  '', ''
            if(i + 1 < self.current_level_len) : next_step = current_level[i+ 1]
            if(i + 2 < self.current_level_len) : second_next_step = current_level[i+ 2]

            #not gonna die tonight!
            if(next_step != ''):
                if (next_step == '_'):
                    steps += 1
                elif (next_step == 'G' and actions[i] == '1'):
                    steps += 1
                elif (next_step == 'L' and actions[i] == '2'):
                    steps += 1
            
            if(second_next_step != ''):
                if(second_next_step == 'D' and  actions[i] == '1'  and actions[i+1] == '1'):
                    step +=1
            
            #wining
            if(next_step != ''):
                if (next_step == '_'):
                    wining = False
                elif (next_step == 'G' and actions[i] != '1'):
                    wining = False
                elif (next_step == 'L' and actions[i] != '2'):
                    wining = False
            if(second_next_step != ''):
                if(second_next_step == 'D' and  (actions[i] != '1'  or actions[i+1] != '1')):
                    wining = False
            
            #mushroom is always good
            if(i>0):
                if(current_step == 'M' and actions[i-1] != '1'):
                    mushroom_point +=1
            
            #jump before end
            if(i + 1 ==  self.current_level_len):
                if(actions[i] == '1'):
                    jump_before_end = True

            #additional jumps
            if(actions[i] == '1'):
                if (next_step == '_'):
                    not_a_good_jump += 1
                elif (next_step == 'L'):
                    not_a_good_jump += 1

            #killing G
            if(actions[i] == '1'):
                if (next_step != 'L'):
                    if (second_next_step == 'G' and actions[i+1] != '0'):
                        killed_gumpas_count += 1

        score += 0.1 * alive_steps
        score += 0.3 * mushroom_point
        score += 0.1 * killed_gumpas_count
        score -= 0.1 * not_a_good_jump
        score += 0.1  if(jump_before_end) else 0 
        score += 0.4  if(wining) else 0 

        return score
    

g = Game(["____G__L__", "___G_M___L_"])
g.load_next_level()

# This outputs (False, 4)
print(g.get_score("0000000000"))
