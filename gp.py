import tree1
import tree2
import read_in
import sys
import random
import copy
import math

# ISSUES:
# - Crossover/mutation is making the functions really big - how can we stop this?
# - Normalization of the fitness - is this correct?
# - Penalizing for larger trees in fitness / divide by size - is there a better way?
# - Full tree method - why are they so large?
# - Fitness function - why are we getting the same fitness for multiple functions across generations?
# - Should fitness really be between 0 and 1?

# ACTION PLAN:
# - Converge an equation please

GENERATIONS = 50
POP_SIZE = 100
CROSSOVER_PERCENT = 0.9  # crossover rate
DUPLICATE_PERCENT = 0.09
MUTATE_PERCENT = 0.01

def set_up_data(dataset):
    if dataset == 1:
        return read_in.dataset1()
    else:
        return read_in.dataset2()

def fitness1(func, x_training, y_training, fitness_indexes):
    fitness = 0.0
    for i in fitness_indexes:  # NOTE: RUNNING ON HALF DATA, randomized 500 for each generartion or try on more
        diff_squared = (abs(func.compute_tree(x_training[i]) - y_training[i]))**2
        fitness += diff_squared
    size = tree1.tree_len(func)
    fitness = (fitness * (1.1 ** size)) / len(x_training)
    # fitness = fitness / len(x_training)

    if not (math.isnan(fitness)):
        return 1.0 / fitness
    else:
        return float("inf")

def fitness2(func, x1_training, x2_training, x3_training, y_training):
    fitness = 0.0
    for i in range(500):  # NOTE: RUNNING ON HALF DATA
        diff_squared = (abs(func.compute_tree(x1_training[i], x2_training[i], x3_training[i]) - y_training[i]))**2
        fitness += diff_squared
    # size = tree2.tree_len(func)
    # fitness = (fitness * size) /len(x1_training)
    fitness = fitness / len(x1_training)

    if not (math.isnan(fitness)):
        return 1.0 / fitness
    else:
        return float("inf")

def make_wheel(fitnesses):
    sum_fitness = 0
    for f in fitnesses:
        sum_fitness += f.fitness
    roulette = {f: (f.fitness / sum_fitness) for f in fitnesses}
    return roulette

def fitness_prop_selection(fitnesses, roulette):
    max_ = sum(roulette.values())
    pick = random.uniform(0, max_)
    current = 0
    for tree, fitness in roulette.items():
        current += fitness
        if current > pick:
            return tree

def dataset1(population, training_df, check_df, TRAINING):
    current_gen = []
    best_func = None
    best_fitness = 0
    best_gen = 0

    x_training = training_df['x'].tolist()
    y_training = training_df['f(x)'].tolist()
    x_check = check_df['x'].tolist()
    y_check = check_df['f(x)'].tolist()


    fitness_indexes = []
    for i in range(500):
        fitness_indexes.append(random.randint(0, len(x_training)))
    # Find fitness for each function in first generation
    for func in population:
        # func.print_tree()
        func.fitness = fitness1(func, x_training, y_training, fitness_indexes)
        if func.fitness != float("inf") and not math.isnan(func.fitness) and func not in current_gen:
            current_gen.append(func)

    for gen in range(GENERATIONS):
    
        for i in range(500):
            fitness_indexes.append(random.randint(0, len(x_training)))
        # print("starting gen")
        nextgen_population = []
        xo_parent_num = int(POP_SIZE * CROSSOVER_PERCENT)
        dupl_parent_num = int(POP_SIZE*DUPLICATE_PERCENT)
        mut_parent_num = int(POP_SIZE * MUTATE_PERCENT)
        roulette = make_wheel(current_gen)
        for _ in range(xo_parent_num):
            xo_parent1 = fitness_prop_selection(current_gen, roulette)
            xo_parent2 = fitness_prop_selection(current_gen, roulette)
            xo_child = tree1.crossover(xo_parent1, xo_parent2)
            xo_child.fitness = fitness1(xo_child, x_training, y_training, fitness_indexes)
            xo_parent1.fitness = fitness1(xo_parent1, x_training, y_training, fitness_indexes)
            if (xo_child.fitness < xo_parent1.fitness):
                nextgen_population.append(xo_parent1)
            elif(xo_child.fitness < xo_parent2.fitness):
                nextgen_population.append(xo_parent2)
            else:
                nextgen_population.append(xo_child)
        for _ in range(mut_parent_num):
            mut_parent = fitness_prop_selection(current_gen, roulette)
            mut_child = tree1.mutation(mut_parent)
            nextgen_population.append(mut_child)
        for _ in range(dupl_parent_num):
            nextgen_population.append(fitness_prop_selection(current_gen, roulette))

        max_fitness = 0
        for func in nextgen_population:
            # func.print_tree()
            func.fitness = fitness1(func, x_training, y_training, fitness_indexes)
            # print("fitness = ", func.fitness)
            if func.fitness != float("inf"):
                    # print(func.fitness)
                # fitnesses.append(func)
                if func.fitness > max_fitness:
                    max_fitness = func.fitness
                    f = func
                    # print('found max')
                    # func.print_tree()
        # print('generated new fitneses')


# print fitness and diversity, research to track diversity
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            # best_gen = gen
            best_func = copy.deepcopy(f)
            # print("________________________")
            # print("gen:", gen, ", best_fitness:", best_fitness, ", best_func:")
            # # print(tree.tree_len(best_of_run))
            # best_func.print_tree()
            # print(best_func.tree_string())
        current_gen = nextgen_population
    check_fitness = fitness1(best_func, x_check, y_check)

    return best_func, check_fitness

def dataset2(population, training_df, check_df, TRAINING):
    current_gen = []
    best_func = None
    best_fitness = 0
    best_gen = 0

    x1_training = training_df['x1'].tolist()
    x2_training = training_df['x2'].tolist()
    x3_training = training_df['x3'].tolist()
    y_training = training_df['f(x1,x2,x3)'].tolist()
    x1_check = check_df['x1'].tolist()
    x2_check = check_df['x2'].tolist()
    x3_check = check_df['x3'].tolist()
    y_check = check_df['f(x1,x2,x3)'].tolist()

    # Find fitness for each function in first generation
    for func in population:
        # func.print_tree()
        func.fitness = fitness2(func, x1_training, x2_training, x3_training, y_training)
        if func.fitness != float("inf") and not math.isnan(func.fitness) and func not in current_gen:
            current_gen.append(func)

    for gen in range(GENERATIONS):
        # print("starting gen")
        nextgen_population = []
        xo_parent_num = int(POP_SIZE * CROSSOVER_PERCENT)
        dupl_parent_num = int(POP_SIZE*DUPLICATE_PERCENT)
        mut_parent_num = int(POP_SIZE * MUTATE_PERCENT)
        roulette = make_wheel(current_gen)
        for _ in range(xo_parent_num):
            xo_parent1 = fitness_prop_selection(current_gen, roulette)
            xo_parent2 = fitness_prop_selection(current_gen, roulette)
            xo_child = tree2.crossover(xo_parent1, xo_parent2)
            xo_child.fitness = fitness2(xo_child, x1_training, x2_training, x3_training, y_training)
            xo_parent1.fitness = fitness2(xo_parent1, x1_training, x2_training, x3_training, y_training)
            if (xo_child.fitness < xo_parent1.fitness):
                nextgen_population.append(xo_parent1)
            elif(xo_child.fitness < xo_parent2.fitness):
                nextgen_population.append(xo_parent2)
            else:
                nextgen_population.append(xo_child)
        for _ in range(mut_parent_num):
            mut_parent = fitness_prop_selection(current_gen, roulette)
            mut_child = tree2.mutation(mut_parent)
            nextgen_population.append(mut_child)
        for _ in range(dupl_parent_num):
            nextgen_population.append(fitness_prop_selection(current_gen, roulette))

        max_fitness = 0
        for func in nextgen_population:
            # func.print_tree()
            func.fitness = fitness2(func, x1_training, x2_training, x3_training, y_training)
            if func.fitness != float("inf"):
                    # print(func.fitness)
                # fitnesses.append(func)
                if func.fitness > max_fitness:
                    max_fitness = func.fitness
                    f = func
                    # print('found max')
                    # func.print_tree()
        # print('generated new fitneses')

        if max_fitness > best_fitness:
            best_fitness = max_fitness
            # best_gen = gen
            best_func = copy.deepcopy(f)
            # print("________________________")
            # print("gen:", gen, ", best_fitness:", best_fitness, ", best_func:")
            # print(tree.tree_len(best_of_run))
            # best_func.print_tree()
            # print(best_func.tree_string())
        current_gen = nextgen_population
    check_fitness = fitness2(best_func, x1_check, x2_check, x3_check, y_check)

    return best_func, check_fitness

def main():

    # read in dataset1 or dataset2 based on command line argument 1 or 2
    dataset = set_up_data(int(sys.argv[1]))
    dataset_len = dataset.shape[0]
    TRAINING = int((dataset_len * 2) / 3)  # 2/3 of dataset points for training

    training_df = dataset[1:TRAINING]
    check_df = dataset[TRAINING:]

    # # tester:
    # population= tree.init_population()
    # dataset1(population, training_df, check_df, TRAINING)

    equations = []
    fitnesses = []
    for _ in range(1, 11):
        if int(sys.argv[1]) == 1:
            # Create first generation of 1000 trees/functions in a list
            population = tree1.init_population()
            equation, fitness = dataset1(population, training_df, check_df, TRAINING)
            equations.append(equation)
            fitnesses.append(fitness)
        else:
            # Create first generation of 1000 trees/functions in a list
            population = tree2.init_population()
            equation, fitness = dataset2(population, training_df, check_df, TRAINING)
            equations.append(equation)
            fitnesses.append(fitness)

    
    max_fitness = max(fitnesses)
    max_fit_i = fitnesses.index(max_fitness)
    best_equation = equations[max_fit_i]

    print('FINAL ANSWER!')
    best_equation.print_tree()
    print(best_equation.fitness)


if __name__ == "__main__":
    main()
