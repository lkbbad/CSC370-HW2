import tree
import read_in
from statistics import mean
import sys

def fitness(func, x_training, y_training):
    func.fitness = 1 / (mean([abs(func.compute_tree(x_training[i]) - y_training[i]) for i in range(0, len(x_training)-1)]))

def set_up_data(dataset):
    if dataset == 1:
        return read_in.dataset1()
    else: return read_in.dataset2()

def dataset1(population, training_df, check_df, TRAINING):
    fitnesses = []
    best_fit = 0

    x_training = training_df['x'].tolist()
    y_training = training_df['f(x)'].tolist()
    x_check = check_df['x'].tolist()
    y_check = check_df['f(x)'].tolist()

    # Find fitness for each function in first generation
    for func in population:
        fitness(func, x_training, y_training)
        fitnesses.append(func.fitness)
    if max(fitnesses) > best_fit:
        best_fit = max(fitnesses)

    best_tree = population[fitnesses.index(max(fitnesses))]
    print(fitnesses.index(max(fitnesses))) #printing pop index of most fit tree
    best_tree.print_tree() #tree
    print(best_tree.fitness) #fitness of tree, normalized from [0,1]
    print(best_tree.tree_string()) #printing tree equation

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


