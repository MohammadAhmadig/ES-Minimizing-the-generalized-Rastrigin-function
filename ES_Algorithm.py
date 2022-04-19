import sys
from random import Random
from time import time
from math import *
from configuration import *

def Chromosome(rand, dimension):
    return [[rand.normalvariate(0, 1) for i in range(dimension)],
            [rand.uniform(-5.12, 5.12) for i in range(dimension)]]

def Parent_selection(rand):
    global population
    if selection:
	parents = [population[rand.randint(0, len(population) - 1)] for _ in range(TournomentSize)]
        parents.sort(key=fitness)
        parent1, parent2 = parents[0], parents[1]
    else:
        parent1 = population[rand.randint(0, len(population) - 1)]
        parent2 = population[rand.randint(0, len(population) - 1)]
        
    return parent1, parent2

def Recombination(rand):
    global n, population
    if x_over_type == 1:
        parent1, parent2 = Parent_selection(rand)
        offspring = [[i for i in parent1[0]], [i for i in parent1[1]]]
        for i in range(len(parent1[0])):
            if rand.randint(0, 1):
                offspring[0][i] = parent2[0][i]
                offspring[1][i] = parent2[1][i]
    elif x_over_type == 2:
        offspring = [[0] * n, [0] * n]
        for i in range(n):
            parent1, parent2 = Parent_selection(rand)
            if rand.randint(0, 1):
                offspring[0][i] = parent2[0][i]
                offspring[1][i] = parent2[1][i]
            else:
                offspring[0][i] = parent1[0][i]
                offspring[1][i] = parent1[1][i]    
    elif x_over_type == 3:
        parent1, parent2 = Parent_selection( rand)
        offspring = [[0.5 * (parent1[0][i] + parent2[0][i]) for i in range(len(parent1[0]))],
                 [0.5 * (parent1[1][i] + parent2[1][i]) for i in range(len(parent1[0]))]]
    else :
        offspring = [[0] * n, [0] * n]
        for i in range(n):
            parent1, parent2 = Parent_selection(rand)
            offspring[0][i] = 0.5 * (parent1[0][i] + parent2[0][i])
            offspring[1][i] = 0.5 * (parent1[1][i] + parent2[1][i])
            
    return offspring            
    
    
def Mutation(offspring, rand):
    global n
    eps = sys.float_info.epsilon
    N_all = rand.normalvariate(0, 1)
    N_i = [rand.normalvariate(0, 1) for _ in range(n)]
    offspring[0] = [offspring[0][i] * exp(tau_prim * N_all + tau * N_i[i]) for i in range(n)]
    for i in range(n):
	if abs(offspring[0][i]) < eps:
	    offspring[0][i] = eps
	else:
	    offspring[0][i] = abs(offspring[0][i])
    offspring[1] = [(offspring[1][i] + offspring[0][i] * N_i[i]) for i in range(n)]
    
def Survival_Selection(offsprings):
    global population
    if Forget_parents:
        offsprings.sort(key=fitness)
        return offsprings[:Pop_Size]
    else:
        offsprings = population + offsprings
        offsprings.sort(key=fitness)
        return offsprings[:Pop_Size]
   
tau = 1 / sqrt(2 * n)
tau_prim = 1 / sqrt(2 * sqrt(n))

population = []
generation = 0
offsprings_size = Pop_Size * 7

Rastrigin_Function = lambda X: n * A + sum([(x ** 2 - A * cos(2 * pi * x)) for x in X])
fitness = lambda offspring: Rastrigin_Function(offspring[1])   

rnd = Random()
rnd.seed(int(time()))
population = [Chromosome(rnd, n) for _ in range(Pop_Size)]
    
while ( generation < max_generation and fitness(population[0]) != 0):
    generation += 1
    offsprings = [Recombination(rnd) for _ in range(offsprings_size)]    
    for offspring in offsprings: Mutation(offspring, rnd)
    population = Survival_Selection(offsprings)
    print "generation of " , generation 
    print "best Rastrigin value is " , fitness(population[0])
    
print("---------------------------------------\n")
print " global minimum of the Rastrigin: ", fitness(population[0])
print " Chromosome of global minimum: ",population[0]
print("\n---------------------------------------")
   

