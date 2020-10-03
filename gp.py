import tree
import read_in
from statistics import mean
import sys
import random
import copy

TOURNAMENT_SIZE = 5
GENERATIONS = 50
POP_SIZE = 1000 

def fitness(func, x_training, y_training):
    func.fitness = 1 / (mean([abs(func.compute_tree(x_training[i]) - y_training[i]) for i in range(0, len(x_training)-1)]))

def selection(population, fitnesses): # select one individual using tournament selection
    tournament = [random.randint(0, len(population)-1) for i in range(TOURNAMENT_SIZE)] # select tournament contenders
    tournament_fitnesses = [fitnesses[tournament[i]] for i in range(TOURNAMENT_SIZE)]
    return copy.deepcopy(population[tournament[tournament_fitnesses.index(max(tournament_fitnesses))]]) 

def set_up_data(dataset):
    if dataset == 1:
        return read_in.dataset1()
    else: return read_in.dataset2()

def dataset1(population, training_df, check_df, TRAINING):
    fitnesses = []
    best_of_run = None
    best_of_run_f = 0
    best_of_run_gen = 0

    x_training = training_df['x'].tolist()
    y_training = training_df['f(x)'].tolist()
    x_check = check_df['x'].tolist()
    y_check = check_df['f(x)'].tolist()

    # Find fitness for each function in first generation
    for func in population:
        fitness(func, x_training, y_training)
        fitnesses.append(func.fitness)
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
            parent1 = selection(population, fitnesses)
            print("original")
            parent1.print_tree()
            parent2 = selection(population, fitnesses)
            print("original2")
            parent2.print_tree()
            parent1.crossover(parent2)
            print("cross")
            parent1.print_tree()
            parent1.mutation()
            print("mutate")
            parent1.print_tree()
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



