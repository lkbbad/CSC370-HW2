import tree
import read_in
import sys
import random
import copy
import math

## ISSUES: 
##  - Crossover/mutation is making the functions really big - how can we stop this?
##  - Normalization of the fitness - is this correct? 
##  - Penalizing for larger trees in fitness / divide by size - is there a better way?
##  - Full tree method - why are they so large?
##  - Fitness function - why are we getting the same fitness for multiple functions across generations?
##  - Should fitness really be between 0 and 1?

GENERATIONS = 1000
POP_SIZE = 500
CROSSOVER_PERCENT = 0.9  # crossover rate

def set_up_data(dataset):
    if dataset == 1:
        return read_in.dataset1()
    else: return read_in.dataset2()

def fitness(func, x_training, y_training):
    fitness = 0.0
    for i in range(int(len(x_training)/2)): # NOTE: RUNNING ON HALF DATA
        diff_squared = (abs(func.compute_tree(x_training[i]) - y_training[i]))**2
        fitness += diff_squared

    size = tree.tree_len(func)
    fitness = (fitness * size) /len(x_training)

    if not (math.isnan(fitness)):
        return 1.0 / fitness
    else: return float("inf")

def make_wheel(fitnesses):
    sum_fitness = 0
    for f in fitnesses:
        sum_fitness += f.fitness
    roulette = {f : (f.fitness / sum_fitness) for f in fitnesses}
    return roulette

def fitness_prop_selection(fitnesses, roulette):
    max = sum(roulette.values())
    pick = random.uniform(0, max)
    current = 0
    for tree, fitness in roulette.items():
        current += fitness
        if current > pick:
            return tree

def dataset1(population, training_df, check_df, TRAINING):
    fitnesses = []
    best_func = None
    best_fitness = 0
    best_gen = 0

    x_training = training_df['x'].tolist()
    y_training = training_df['f(x)'].tolist()
    x_check = check_df['x'].tolist()
    y_check = check_df['f(x)'].tolist()

    # Find fitness for each function in first generation
    for func in population:
        # func.print_tree()
        func.fitness = fitness(func, x_training, y_training)
        if func.fitness != float("inf"): 
            fitnesses.append(func)

    for gen in range(GENERATIONS):
        # print("starting gen")
        nextgen_population=[]
        xo_parent_num = int(POP_SIZE * CROSSOVER_PERCENT)
        mut_parent_num = int(POP_SIZE - xo_parent_num)
        roulette = make_wheel(fitnesses)
        for j in range(xo_parent_num):
            xo_parent1 = fitness_prop_selection(fitnesses, roulette)
            xo_parent2 = fitness_prop_selection(fitnesses, roulette)
            xo_parent1.crossover(xo_parent2)
            nextgen_population.append(xo_parent1)
        for k in range(mut_parent_num):
            mut_parent = fitness_prop_selection(fitnesses, roulette)
            mut_parent.mutation()
            nextgen_population.append(mut_parent)
        # print("finished pop")

        max_fitness = 0
        for func in nextgen_population:
            # func.print_tree()
            func.fitness = fitness(func, x_training, y_training)
            # print("fitness = ", func.fitness)
            if func.fitness != float("inf"):
                    # print(func.fitness)
                # fitnesses.append(func)
                if func.fitness > max_fitness:
                    max_fitness = func.fitness
                    f = func
                    # print('found max')
        # print('generated new fitneses')

        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_gen = gen
            best_func = copy.deepcopy(f)
            print("________________________")
            print("gen:", gen, ", best_fitness:", round(best_fitness,3), ", best_func:")
            # print(tree.tree_len(best_of_run))
            best_func.print_tree()
            # print(best_func.tree_string())
            print(best_func.compute_tree(-0.66), " should be 18")
            print(best_func.compute_tree(2.99), " should be 5") 

        if best_fitness >= 1: break

def dataset2(population, training_df, check_df, TRAINING):
    x1_training = training_df['x1'].tolist()
    x2_training = training_df['x2'].tolist()
    x3_training = training_df['x3'].tolist()
    y_training = training_df['f(x1,x2,x3)'].tolist()
    x1_check = check_df['x1'].tolist()
    x2_check = check_df['x2'].tolist()
    x3_check = check_df['x3'].tolist()
    y_check = check_df['f(x1,x2,x3)'].tolist()

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



