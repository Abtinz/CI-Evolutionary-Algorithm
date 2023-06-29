import copy
import os
import random
import time

import numpy as np
from matplotlib import pyplot as plt

class Game:
    def __init__(self, levels,iterations_number,chromosome_number):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps
         # store current levels index for processing them in order...
        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0
        self.iterations_number = iterations_number
        self.chromosome_number = chromosome_number
    
    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    #making the first population for algorithm
    def population(self,gens_count, chromosome_count):

        chromosome = [[np.random.choice(np.arange(0, 3), p=[0.5, 0.2, 0.3]) for i in range(gens_count)] for j in range(chromosome_count)]
        chromosomes_string = []
        for i in range(chromosome_count):
            chromosome_string = ''.join(str(gene) for gene in chromosome[i])
            chromosomes_string.append(chromosome_string)

        return chromosome , chromosomes_string
    
    def assessing_competency(self, actions):
        # Get an action sequence and determine the steps taken/score
        # Return a tuple, the first one indicates if these actions result in victory
        # and the second one shows the steps taken
        
        current_level = self.levels
        alive_steps = 0
        steps = 0
        score = 0
        mushroom_point = 0
        wining = True
        jump_before_end = False
        not_a_good_jump = 0
        killed_gumpas_count = 0
        
        for i in range(len(current_level)):
            current_step = current_level[i]
            next_step, second_next_step =  '', ''
            if(i + 1 < len(current_level)) : next_step = current_level[i+ 1]
            if(i + 2 < len(current_level)) : second_next_step = current_level[i+ 2]

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
                    steps +=1
            
            #wining
            if(next_step != ''):  
                if (next_step == 'G' and actions[i-1] != '1'):
                    wining = False
                elif (next_step == 'L' and actions[i-1] != '2'):
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
                    if (second_next_step == 'G' and actions[i+1] == '0'):
                        killed_gumpas_count += 1
        
        score += 1 * alive_steps
        score += 6 * mushroom_point
        score += 8 * killed_gumpas_count
        score -= 2 * not_a_good_jump
        score += 3  if(jump_before_end) else 0
        score += 8  if(wining) else 0

        return score

    # will help to perform selection operation on the chromosomes
    def selection(self,chromosomes, scores):
    
        for i in range(len(chromosomes)):
            for j in range(0, len(chromosomes) - i - 1):
                if scores[j] > scores[j + 1]:
                    scores[j], scores[j + 1] = scores[j + 1], scores[j] 
                    chromosomes[j], chromosomes[j + 1] = chromosomes[j + 1], chromosomes[j]
        length = len(chromosomes)
        half_length = int(length/2)
        return chromosomes[half_length:length]

    def crossover(self, chromosome, num):
        
    
        new_generation = []
        survived_parents_count  = int(num/10)
        child_counts = num - survived_parents_count
        
        for i in range(child_counts):
            
            #selecting random parents
            first_parent_index = random.randint(0, len(chromosome) - 1)
            second_parent_index = random.randint(0, len(chromosome) - 1)
            first_parent = chromosome[first_parent_index]
            second_parent = chromosome[second_parent_index]

            #we need deep copy because the genetic algorithm modifies the chromosomes in place!
            first_child = first_parent.copy()
            second_child = second_parent.copy()

            #the separation mode is from 1 to second last index(its a combination of two indexes)
            first_point = random.randint(1, len(first_parent) - 2)
            second_point = random.randint(1, len(second_parent) - 2)

            if second_point > first_point:
                first_child = first_parent[:first_point] + second_parent[first_point:second_point] + first_parent[second_point:]
                second_child = second_parent[:first_point] + first_parent[first_point:second_point] + second_parent[second_point:]

            elif second_point == first_point:
                first_child = first_parent[:first_point] + second_parent[first_point:]
                second_child = second_parent[:first_point] + first_parent[first_point:]

            else:
                first_child = first_parent[:second_point] + second_parent[second_point:first_point] + first_parent[first_point:]
                second_child = second_parent[:second_point] + first_parent[second_point:first_point] + second_parent[first_point:]
            
            point1 = self.assessing_competency(first_child)
            point2 = self.assessing_competency(second_child)

            if point1 > 0 and point2 > 0:
                if point1 > point2:
                    new_generation.append(first_child)
                elif point2 > point1:
                    new_generation.append(second_child)
                else:
                    new_generation.append(first_child)
                    new_generation.append(second_child)
        
        # Select the top 10% of chromosomes to be copied to the new generation
        for i in range(survived_parents_count):
            survived_parent = random.randint(0, len(chromosome) - 1)
            new_generation.append(chromosome[survived_parent])

        return new_generation

    # Define a function to perform mutation on the chromosomes
    def mutation(self,chromosome,iteration_percent):
       
        # Iterate over 30% of the chromosomes -> the mutation is limited
        random_mutation_term = random.randint(1,3) #how many gens should be changed
        temp = 0
        while iteration_percent > 0:
            index = random.randint(0, len(chromosome) - 1)
            # Select a random point for mutation operation
            point = random.randint(0, len(chromosome[index]) - 1)
            # Perform mutation on the chromosome
            if temp != random_mutation_term:
                if chromosome[index][point] == "1":
                    chromosome[index][point] = "0"
                else:
                    chromosome[index][point] = "1"
                temp -=-1
            else:
                temp = 0
                iteration_percent -= 1 
      
        return chromosome

    def plot_function(self, max_scores, min_scores, average_scores,name):
        plt.plot(max_scores, label="max")
        plt.plot(min_scores, label="min")
        plt.plot(average_scores, label="average")
        plt.xlabel("generation")
        plt.ylabel("assessing competition points")
        plt.legend()
        plt.savefig('C:/Users/abt/Desktop/CI_P3/attachments/plots/est.png')

    def scores_evaluation(self, scores):
        scores_np = np.asarray(scores)
        return scores_np.max(), scores_np.min(), scores_np.mean()
        

def main(level_file_route , chromosomes_number , iterations_count,plot_address):

    
    first_itration = True
    level = open(level_file_route, 'r').readline()
    gens_count = len(level)
    game= Game(levels= level,chromosome_number= chromosomes_number, iterations_number= iterations_count)
    game.load_next_level()
    next_generation_chromosomes = []

    minimum_points = []
    maximum_points = []
    average_points = []
    while iterations_count > 0 :

        if not first_itration:
            chromosomes_string = []
            for i in range(len(next_generation_chromosomes)):
                chromosomes_string.append(''.join(str(gene) for gene in next_generation_chromosomes[i]))
            chromosomes = next_generation_chromosomes
        else:
            chromosomes  , chromosomes_string = game.population(gens_count, chromosomes_number)
            first_itration = False
        
        scores = []
        for i in range(len(chromosomes_string)):
            scores.append(game.assessing_competency(chromosomes_string[i]))
        
        selected_chromosomes = game.selection(chromosomes, scores)
        new_generation = game.crossover(selected_chromosomes, 200)
        iteration_percent = 0.3 * len(new_generation)
        next_generation_chromosomes = game.mutation(new_generation,iteration_percent)
        maximum, minimum, average = game.scores_evaluation(scores)

        minimum_points.append(minimum)
        maximum_points.append(maximum)
        average_points.append(average)

        iterations_count -=1

    
    
    game.plot_function(maximum_points ,minimum_points, average_points, plot_address)   
        

#main(level_file_route = "./levels/level4.txt",  chromosomes_number= 350, iterations_count=20)
main(level_file_route = "./levels/level5.txt",  chromosomes_number= 350, iterations_count=20, plot_address = './plots/level5.png')
main(level_file_route = "./levels/level6.txt",  chromosomes_number= 350, iterations_count=20 ,plot_address = './plots/level6.png')
#main(level_file_route = "./levels/level7.txt",  chromosomes_number= 350, iterations_count=20)

