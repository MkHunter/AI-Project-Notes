from deap import base
from deap import creator
from deap import tools

import random
import array

import numpy as np

import elitism

# Problem parameters:
NUM_OF_QUEENS = 50

# Genetic Algorithm constants:
POPULATION_SIZE = 3000
MAX_GENERATIONS = 1000
HALL_OF_FAME_SIZE = 30
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.1   # probability for mutating an individual

# set the random seed for repeatable results
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

toolbox = base.Toolbox()

# define a single objective, minimizing fitness strategy:
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# create the Individual class based on list of integers:
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

# create an operator that generates randomly shuffled indices:
toolbox.register("randomOrder", random.sample, range(NUM_OF_QUEENS), NUM_OF_QUEENS)

# create the individual creation operator to fill up an Individual instance with shuffled indices:
toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomOrder)

# create the population creation operator to generate a list of individuals:
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

def getattacks(_state):
    state = [x+1 for x in _state]
    n = len(state)
    attacks = 0
    for i in range(0,n):
        X = state[i]
        for j in range(i+1,n):
            Y = state[j]
            if(X-Y == 0):
                attacks+=2
            if(abs(i-j) == abs(X-Y)):
                attacks+=2
    return attacks

# fitness calculation - compute the total distance of the list of cities represented by indices:
def getViolationsCount(individual):
    #print(" INDIVIDUAL : ",str(individual)," ATTACKS : ",getattacks(individual))
    return getattacks(individual),  # return a tuple


toolbox.register("evaluate", getViolationsCount)

# Genetic operators:
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=2.0/NUM_OF_QUEENS)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/NUM_OF_QUEENS)


# Genetic Algorithm flow:
def main():
    # Create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    # Prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    # Define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # Perform the Genetic Algorithm flow with hof feature added:
    population, logbook = elitism.eaSimpleWithElitism(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # Print hall of fame members info:
    print("- Best solutions are:")
    for i in range(HALL_OF_FAME_SIZE):
        print(i, ": ", hof.items[i].fitness.values[0], " -> ", hof.items[i])

if __name__ == "__main__":
    main()
