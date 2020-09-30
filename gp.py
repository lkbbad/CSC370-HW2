import tree
import read_in

# for i in population:
#     print(i.tree_string())
#     print(i.compute_tree(3))
#     print()

def fitness(func, x_training, y_training):
    my_fitness = 0
    for x in range(len(x_training)):
        diff_squared = 0
        try:
            diff_squared = abs(y_training[x]) - (func.compute_tree(x_training[x]))**2
        except:
            func.fitness = float("inf")
            return
        my_fitness += diff_squared
    func.fitness =  my_fitness / len(x_training)


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
    print(population[fitnesses.index(max(fitnesses))].print_tree())
    print(population[fitnesses.index(max(fitnesses))].fitness)

if __name__ == "__main__":
    main()