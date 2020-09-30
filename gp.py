import tree
import read_in
from statistics import mean


# for i in population:
#     print(i.tree_string())
#     print(i.compute_tree(3))
#     print()

def fitness(func, x_training, y_training):

#    for i in range(0, len(x_training)-1):
#        guess = func.compute_tree(x_training[i])
#        print(guess)


    func.fitness = 1 / (mean([abs(func.compute_tree(x_training[i]) - y_training[i]) for i in range(0, len(x_training)-1)]))


#    my_fitness = 0
#    for x in range(len(x_training)):
#        diff_squared = 0
#        try:
#            diff_squared = abs(y_training[x]) - (func.compute_tree(x_training[x]))**2
#        except:
#            func.fitness = float("inf")
#            return
#        my_fitness += diff_squared
#    func.fitness =  my_fitness / len(x_training)


def main():
    # Create population of 1000 trees/functions in a list
    population= tree.init_population()
    dataset1 = read_in.dataset1()
    fitnesses = []
    best_fit = 0
    x_training = dataset1['x'].tolist()
    y_training = dataset1['f(x)'].tolist()

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

if __name__ == "__main__":
    main()


