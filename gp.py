import tree
import read_in
from statistics import mean
import sys
import random
import copy
import math

TOURNAMENT_SIZE = 5
GENERATIONS = 50
POP_SIZE = 10
PROB_MUTATION = 0.1  # probability of perfoming a mutation
CROSSOVER_RATE = 0.9  # crossover rate

def set_up_data(dataset):
    if dataset == 1:
        return read_in.dataset1()
    else: return read_in.dataset2()

def fitness(func, x_training, y_training):
    fitness = 0.0
    for i in range(len(x_training)):
        diff_squared = (func.compute_tree(x_training[i]) - y_training[i])**2
        fitness += diff_squared / len(x_training)
    if not (math.isnan(fitness)):
        return 1.0 / fitness
    else: return float("inf")

# def selection(population, fitnesses): # select one individual using tournament selection
#     tournament = [random.randint(0, len(population)-1) for i in range(TOURNAMENT_SIZE)] # select tournament contenders
#     tournament_fitnesses = [fitnesses[tournament[i]] for i in range(TOURNAMENT_SIZE)]
#     return copy.deepcopy(population[tournament[tournament_fitnesses.index(max(tournament_fitnesses))]]) 

def fitness_prop_selection(fitnesses, population):
    sum_fitness = 0
    for f in fitnesses:
        sum_fitness += f.fitness
    roulette = {f : (f.fitness / sum_fitness) for f in fitnesses}

    max = sum(roulette.values())
    pick = random.uniform(0, max)
    current = 0
    for tree, fitness in roulette.items():
        current += fitness
        if current > pick:
            return tree


def dataset1(population, training_df, check_df, TRAINING):
    fitnesses = []
    # best_of_run = None
    # best_of_run_f = 0
    # best_of_run_gen = 0

    x_training = training_df['x'].tolist()
    y_training = training_df['f(x)'].tolist()
    x_check = check_df['x'].tolist()
    y_check = check_df['f(x)'].tolist()

    # Find fitness for each function in first generation
    for func in population:
        func.fitness = fitness(func, x_training, y_training)
        if func.fitness != float("inf"): 
            fitnesses.append(func)
    # for f in fitnesses:
    #     print(f.fitness)

    # if max(fitnesses) > best_fit:
    #     best_fit = max(fitnesses)

    # best_tree = population[fitnesses.index(max(fitnesses))]
    
    # print(fitnesses.index(max(fitnesses))) #printing pop index of most fit tree
    # best_tree.print_tree() #tree
    # print(best_tree.fitness) #fitness of tree, normalized from [0,1]
    # print(best_tree.tree_string()) #printing tree equation

    for gen in range(1):        
        nextgen_population=[]
        for i in range(1):
            xo_parent_num = int(int(POP_SIZE / 2) * CROSSOVER_RATE)
            mut_parent_num = int(POP_SIZE - (2 * xo_parent_num))
            for j in range(xo_parent_num):
                xo_parent1 = fitness_prop_selection(fitnesses, population)
                xo_parent2 = fitness_prop_selection(fitnesses, population)
                print(xo_parent1, xo_parent2)
            for k in range(mut_parent_num):
                mut_parent = fitness_prop_selection(fitnesses, population)
                print(mut_parent)

    #         parent1 = selection(population, fitnesses)
    #         parent1.print_tree()
    #         parent2 = selection(population, fitnesses)
    #         parent2.print_tree()
    #         parent1.crossover(parent2)
    #         parent1.print_tree()
    #         parent1.mutation()
    #         parent1.print_tree()
    #         nextgen_population.append(parent1)
    #     population=nextgen_population
    #     fitnesses = [fitness(population[i], x_training, y_training) for i in range(POP_SIZE)]
    #     print(fitnesses)
    #     if max(fitnesses) > best_of_run_f:
    #         best_of_run_f = max(fitnesses)
    #         best_of_run_gen = gen
    #         best_of_run = copy.deepcopy(population[fitnesses.index(max(fitnesses))])
    #         print("________________________")
    #         print("gen:", gen, ", best_of_run_f:", round(max(fitnesses),3), ", best_of_run:") 
    #         best_of_run.print_tree()
    #     if best_of_run_f == 1: break   
    
    # print("\n\n_________________________________________________\nEND OF RUN\nbest_of_run attained at gen " + str(best_of_run_gen) +\
    #       " and has f=" + str(round(best_of_run_f,3)))
    # best_of_run.print_tree()

# def dataset2(population, training_df, check_df, TRAINING):
#     x1_training = training_df['x1'].tolist()
#     x2_training = training_df['x2'].tolist()
#     x3_training = training_df['x3'].tolist()
#     y_training = training_df['f(x1,x2,x3)'].tolist()
#     x1_check = check_df['x1'].tolist()
#     x2_check = check_df['x2'].tolist()
#     x3_check = check_df['x3'].tolist()
#     y_check = check_df['f(x1,x2,x3)'].tolist()

def main():
    # Create first generation of 1000 trees/functions in a list
    population= tree.init_population()

    # read in dataset1 or dataset2 based on command line argument 1 or 2
    dataset = set_up_data(int(sys.argv[1]))
    dataset_len = dataset.shape[0]
    TRAINING = int((dataset_len * 2) / 3) # 2/3 of dataset points for training
 
    training_df = dataset[1:TRAINING]
    check_df = dataset[TRAINING:]
    
    if int(sys.argv[1]) == 1:
        dataset1(population, training_df, check_df, TRAINING)
    else: 
        dataset2(population, training_df, check_df, TRAINING)

if __name__ == "__main__":
    main()



