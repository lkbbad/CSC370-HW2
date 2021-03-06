"""
Genetic programming-based symbolic regression implementation.
Authors: Caroline Sigl and Lindy Bustabad
"""

import tree1
import tree2
import read_in
import sys
import random
import copy
import math
import matplotlib.pyplot as plt
import numpy as np

GENERATIONS = 51
POP_SIZE = 500
CROSSOVER_PERCENT = 0.9  
DUPLICATE_PERCENT = 0.1
MUTATE_PERCENT = 0.001

def set_up_data(dataset):
    """
    Initializes datasets based on command line arguments.
    """
    if dataset == 1:
        return read_in.dataset1()
    else:
        return read_in.dataset2()


def fitness1(func, x_training, y_training):
    """
    Fitness function for dataset1: mean squared error, includes penalty factor for deeper trees.
    """
    fitness = 0.0
    depth = tree1.tree_depth(func)
    if depth > 10: # if deeper than 10, fitness is 0 and the tree will not become selected
        return 0, sys.maxsize
    for i in range(len(x_training)):
        diff_squared = (abs(func.compute_tree(x_training[i]) - y_training[i]))**2
        fitness += diff_squared
    mse = fitness / len(x_training)
    fitness = (fitness* 1.05**depth) / len(x_training)

    if not (math.isnan(fitness)):
        return (1.0 / fitness), mse
    else:
        return 0, sys.maxsize


def fitness2(func, x1_training, x2_training, x3_training, y_training):
    """
    Fitness function for dataset2: mean squared error, includes penalty factor for deeper trees.
    """
    fitness = 0.0
    depth = tree2.tree_depth(func)
    if depth > 10: # if deeper than 10, fitness is 0 and the tree will not become selected
        return 0, sys.maxsize
    for i in range(len(x1_training)):  
        diff_squared = (abs(func.compute_tree(x1_training[i], x2_training[i], x3_training[i]) - y_training[i]))**2
        fitness += diff_squared
    mse = fitness / len(x1_training) # Calculte MSE
    fitness = (fitness* 1.05**depth) / len(x1_training)

    if not (math.isnan(fitness)):
        return (1.0 / fitness), mse
    else:
        return 0, sys.maxsize


def make_wheel(fitnesses):
    """
    Fitness proportionate selection: generate "roulette" wheel of selection probabilities based on fitnesses of functions. 
    """
    sum_fitness = 0.0
    for f in fitnesses:
        sum_fitness += f.fitness
    roulette = {f: (f.fitness / sum_fitness) for f in fitnesses}
    return roulette


def fitness_prop_selection(fitnesses, roulette):
    """
    Fitness proportionate selection: generates random number and selects individual by fitness probability. 
    """
    max_ = sum(roulette.values())
    pick = random.uniform(0, max_)
    current = 0.0
    for tree, fitness in roulette.items():
        current += fitness
        if current > pick:
            return tree


def dataset1(population, training_df, check_df, TRAINING):
    """
    Genetic programming algorithm evolution for dataset1.
    """
    current_gen = []
    best_func = None
    best_fitness = 0

    x_training = training_df['x'].tolist()
    y_training = training_df['f(x)'].tolist()
    x_check = check_df['x'].tolist()
    y_check = check_df['f(x)'].tolist()
    
    # Find fitnesses for each individual in initial population
    for func in population:
        func.fitness, func.mse = fitness1(func, x_training, y_training)
        # Initial grooming of population for "bad" individuals
        if func.fitness != 0 and not math.isnan(func.fitness) and func not in current_gen:
            if func.fitness > best_fitness:
                best_func = func
                best_fitness = func.fitness
            current_gen.append(func)
    
    # Filling in the rest of the initial population after grooming
    while(len(current_gen) < POP_SIZE):
        population = tree1.init_population(2)
        for func in population:
            func.fitness, func.mse = fitness1(func, x_training, y_training)
            if func.fitness != 0 and not math.isnan(func.fitness) and func not in current_gen:
                current_gen.append(func)
                if func.fitness > best_fitness:
                    best_func = func
                    best_fitness = func.fitness
    print("Fitness is: ", best_fitness)
    print("MSE is: ", best_func.mse)
    best_func.print_tree()

    for gen in range(GENERATIONS):
        print("Generation : ", gen)
        nextgen_population = []
        xo_parent_num = int(POP_SIZE * CROSSOVER_PERCENT)
        dupl_parent_num = int(POP_SIZE * DUPLICATE_PERCENT)
        mut_parent_num = int(POP_SIZE * MUTATE_PERCENT)
        roulette = make_wheel(current_gen)
        for _ in range(xo_parent_num):
            # Select parents for crossover
            xo_parent1 = fitness_prop_selection(current_gen, roulette)
            xo_parent2 = fitness_prop_selection(current_gen, roulette)
            xo_child, xo_child2 = tree1.crossover(xo_parent1, xo_parent2)
            xo_child.fitness, xo_child.mse = fitness1(xo_child, x_training, y_training)
            xo_child2.fitness, xo_child2.mse = fitness1(xo_child2, x_training, y_training)
            # Select the most fit child
            if xo_child2.fitness > xo_child.fitness:
                xo_child = xo_child2
            xo_child.fitness, xo_child.mse = fitness1(xo_child, x_training, y_training)
            xo_parent1.fitness, xo_parent1.mse = fitness1(xo_parent1, x_training, y_training)
            xo_parent2.fitness, xo_parent2.mse = fitness1(xo_parent2, x_training, y_training)
            # Pseudo-hill climbing: add child into new generation only if more fit than parents
            # Otherwise, add most fit parent
            if (xo_child.fitness < xo_parent1.fitness):
                nextgen_population.append(xo_parent1)
            elif(xo_child.fitness < xo_parent2.fitness):
                nextgen_population.append(xo_parent2)
            else:
                nextgen_population.append(xo_child)
        for _ in range(mut_parent_num):
            # Select parents for mutation
            mut_parent = fitness_prop_selection(current_gen, roulette)
            mut_child = tree1.mutation(mut_parent)
            nextgen_population.append(mut_child)
        for _ in range(dupl_parent_num):
            # Select individuals for duplication
            nextgen_population.append(fitness_prop_selection(current_gen, roulette))

        # Generate fitnesses for new population and select the most fit individual
        for func in nextgen_population:
            func.fitness, func.mse = fitness1(func, x_training, y_training)
            if func.fitness != float("inf"):
                if func.fitness > best_fitness:
                    best_fitness = func.fitness
                    best_func = copy.deepcopy(func)
                    best_func.print_tree()
                    print("Fitness is: ", best_fitness)
                    print("MSE is: ", best_func.mse)

        current_gen = copy.deepcopy(nextgen_population)
    
    check_fitness, best_func.mse = fitness1(best_func, x_check, y_check)

    return best_func, check_fitness, best_func.mse


def dataset2(population, training_df, check_df, TRAINING):
    """
    Genetic programming algorithm evolution for dataset2.
    """
    current_gen = []
    best_func = None
    best_fitness = 0

    x1_training = training_df['x1'].tolist()
    x2_training = training_df['x2'].tolist()
    x3_training = training_df['x3'].tolist()
    y_training = training_df['f(x1,x2,x3)'].tolist()
    x1_check = check_df['x1'].tolist()
    x2_check = check_df['x2'].tolist()
    x3_check = check_df['x3'].tolist()
    y_check = check_df['f(x1,x2,x3)'].tolist()

    # Find fitnesses for each individual in initial population
    for func in population:
        func.fitness, func.mse = fitness2(func, x1_training, x2_training, x3_training, y_training)
        # Initial grooming of population for "bad" individuals
        if func.fitness != 0 and not math.isnan(func.fitness) and func not in current_gen:
            if (func.tree_string().find('x1') != -1) and (func.tree_string().find('x2') != -1) and (func.tree_string().find('x3') != -1):
                if func.fitness > best_fitness:
                    best_func = func
                    best_fitness = func.fitness
                current_gen.append(func)

    while(len(current_gen) < POP_SIZE):
        population = tree2.init_population(2)
        for func in population:
            func.fitness, func.mse = fitness2(func, x1_training, x2_training, x3_training, y_training)
            if func.fitness != 0 and not math.isnan(func.fitness) and func not in current_gen:
                if (func.tree_string().find('x1') != -1) and (func.tree_string().find('x2') != -1) and (func.tree_string().find('x3') != -1):
                    current_gen.append(func)
                    if func.fitness > best_fitness:
                        best_func = func
                        best_fitness = func.fitness
    print("Fitness is: ", best_fitness)
    print("MSE is: ", best_func.mse)
    best_func.print_tree()

    for gen in range(GENERATIONS):
        print("Generation : ", gen)
        nextgen_population = []
        xo_parent_num = int(POP_SIZE * CROSSOVER_PERCENT)
        dupl_parent_num = int(POP_SIZE * DUPLICATE_PERCENT)
        mut_parent_num = int(POP_SIZE * MUTATE_PERCENT)
        roulette = make_wheel(current_gen)
        for _ in range(xo_parent_num):
            # Select parents for crossover
            xo_parent1 = fitness_prop_selection(current_gen, roulette)
            xo_parent2 = fitness_prop_selection(current_gen, roulette)
            xo_child, xo_child2 = tree1.crossover(xo_parent1, xo_parent2)
            xo_child.fitness, xo_child.mse = fitness2(xo_child, x1_training, x2_training, x3_training, y_training)
            xo_child2.fitness, xo_child2.mse = fitness2(xo_child2, x1_training, x2_training, x3_training, y_training)
            # Select the most fit child
            if xo_child2.fitness > xo_child.fitness:
                xo_child = xo_child2
            xo_child.fitness, xo_child.mse = fitness2(xo_child, x1_training, x2_training, x3_training, y_training)
            xo_parent1.fitness, xo_parent1.mse = fitness2(xo_parent1, x1_training, x2_training, x3_training, y_training)
            xo_parent2.fitness, xo_parent2.mse = fitness2(xo_parent2, x1_training, x2_training, x3_training, y_training)
            # Pseudo-hill climbing: add child into new generation only if more fit than parents
            # Otherwise, add most fit parent
            if (xo_child.fitness < xo_parent1.fitness):
                nextgen_population.append(xo_parent1)
            elif(xo_child.fitness < xo_parent2.fitness):
                nextgen_population.append(xo_parent2)
            else:
                nextgen_population.append(xo_child)
        for _ in range(mut_parent_num):
            # Select parents for mutation
            mut_parent = fitness_prop_selection(current_gen, roulette)
            mut_child = tree2.mutation(mut_parent)
            nextgen_population.append(mut_child)
        for _ in range(dupl_parent_num):
            # Select individuals for duplication
            nextgen_population.append(fitness_prop_selection(current_gen, roulette))

        # Generate fitnesses for new population and select the most fit individual
        for func in nextgen_population:
            func.fitness, func.mse = fitness2(func, x1_training, x2_training, x3_training, y_training)
            if func.fitness != float("inf"):
                if func.fitness > best_fitness:
                    best_fitness = func.fitness
                    best_func = copy.deepcopy(func)
                    best_func.print_tree()
                    print("Fitness is: ", best_fitness)
                    print("MSE is: ", func.mse)

        current_gen = copy.deepcopy(nextgen_population)
    
    check_fitness, best_func.mse = fitness2(best_func, x1_check, x2_check, x3_check, y_check)

    return best_func, check_fitness, best_func.mse

def best_func(X):
    """
    Best fit model for dataset1.
    """
    return X * X - 6 * X + 14

def main():
    # Read in dataset1 or dataset2 based on command line argument 1 or 2
    dataset = set_up_data(int(sys.argv[1]))
    dataset_len = dataset.shape[0]
    TRAINING = int((dataset_len * 1) / 3)  # 2/3 of dataset points for training

    training_df = dataset[1:TRAINING]
    check_df = dataset[TRAINING:]

    equations = []
    fitnesses = []
    for _ in range(1, 11):
        if int(sys.argv[1]) == 1:
            # Create first generation of functions
            population = tree1.init_population(POP_SIZE)
            equation, fitness = dataset1(population, training_df, check_df, TRAINING)
            equations.append(equation)
            fitnesses.append(fitness)
        else:
            # Create first generation of functions 
            population = tree2.init_population(POP_SIZE)
            equation, fitness, mse = dataset2(population, training_df, check_df, TRAINING)
            equations.append(equation)
            fitnesses.append(fitness)

    max_fitness = max(fitnesses)
    max_fit_i = fitnesses.index(max_fitness)
    best_equation = equations[max_fit_i]

    print('Symbol regression result: ')
    best_equation.print_tree()
    print("Final fitness is: ", best_equation.fitness)
    print("Final MSE is: ", best_equation.mse)
        
    # MATPLOT LIB CODE
    # my_range = np.arange(-5, 5.0, step=.01)
    
    # # Full dataset
    # fig, ax = plt.subplots()
    # full_df = dataset[1:]
    # x_full = np.array(full_df['x'].tolist(), dtype='float')
    # y_full = np.array(full_df['f(x)'].tolist(), dtype='float')

    # ax.scatter(x_full, y_full,
    #            label='Dataset1 Values', color='C2')

    # ax.plot(my_range, best_func(my_range),
    #         label='Predicted Values', color='C3')

    # ax.set_xlabel('X')
    # ax.set_ylabel('f(x)')
    # ax.legend()
    # plt.suptitle(
    #     'Function f(x) and Dataset1')
    # plt.show()


if __name__ == "__main__":
    main()
