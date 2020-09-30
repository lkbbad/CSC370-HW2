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
            diff_squared = (func.compute_tree(x_training[x]) - y_training[x])**2
        except:
            func.fitness = float("inf")
            return
        my_fitness += diff_squared
    func.fitness =  my_fitness / len(x_training)


def main():
    # Create population of 1000 trees/functions in a list
    population= tree.init_population() 
    dataset1 = read_in.dataset1()
    x_training = dataset1['x'].tolist()
    y_training = dataset1['f(x)'].tolist()
    for func in population:
        fitness(func, x_training, y_training)

if __name__ == "__main__":
    main()