import operator
import random
import copy

POP_SIZE = 500  # population size
MIN_DEPTH = 2    # minimal initial random tree depth
MAX_DEPTH = 4   # maximal initial random tree depth
PROB_MUTATION = 0.75  # probability of perfoming a mutation
CROSSOVER_RATE = 0.8  # crossover rate

def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
def div(x, y):
    try:
        return x/y
    except ZeroDivisionError:
        return 0
operators = [add, sub, mul, div]
terminals = [-2, -1, 1, 2, 'x']

class Tree:
    def __init__(self, body = None, left = None, right = None):
        self.body  = body
        self.left  = left
        self.right = right
        self.fitness = 0
        
    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def __str__(self):
        return str(self.body)

    def node_label(self): # string label
        if (self.body in operators):
            return self.body.__name__
        else:
            return str(self.body)

    def print_tree(self, prefix = ""): # textual printout
        print("%s%s" % (prefix, self.node_label()))
        if self.left:  self.left.print_tree (prefix + "   ")
        if self.right: self.right.print_tree(prefix + "   ")

    def random_tree(self, grow, max_depth, depth = 0):
            # Full method
            if depth < MIN_DEPTH or (depth < MAX_DEPTH and not grow):
                self.body = random.choice(operators)
            elif depth >= MAX_DEPTH:
                self.body = random.choice(terminals)
            else: # intermediate depth, grow
                if random.random() > 0.9:
                    self.body = random.choice(operators)
                else:
                    self.body = random.choice(terminals)
            if self.body in operators:
                self.left = Tree()
                self.left.random_tree(grow, max_depth, depth = depth + 1)
                self.right = Tree()
                self.right.random_tree(grow, max_depth, depth = depth + 1)

    def copy(self):
        return copy.deepcopy(self)

    def tree_string(self):
        if self.body is None: 
            return 0   
        # leaf node 
        if self.left is None and self.right is None: 
            return self.body
        # evaluate left tree 
        left_sum = self.left.tree_string() 
        # evaluate right tree 
        right_sum = self.right.tree_string() 
        # check which operation to apply 
        if self.body == add: 
            return '(' + str(left_sum) + ')' + '+' + '(' + str(right_sum) + ')'
        elif self.body == sub: 
            return '(' + str(left_sum) + ')' + '-' + '(' + str(right_sum) + ')'
        elif self.body == mul: 
            return '(' + str(left_sum) + ')' + '*' + '(' + str(right_sum) + ')'
        else: 
            return '(' + str(left_sum) + ')' + '/' + '(' + str(right_sum) + ')'

    def compute_tree(self, x): 
        if (self.body in operators): 
            try:
                return self.body(self.left.compute_tree(x), self.right.compute_tree(x))
            except:
                return float("inf")
        elif self.body == 'x': return x
        else: return self.body

def mutation(parent):
    rand = random.uniform(0,1)
    if rand > PROB_MUTATION or (not parent.left and not parent.right): # mutate at this node
        if parent.body in operators:
            parent_copy = parent.copy()
            new = random.choice(operators)
            if new != parent_copy.body:
                parent_copy.body = new
                return parent_copy.copy()
            else: return parent_copy.copy()
        else: 
            parent_copy = parent.copy()
            new = random.choice(terminals)
            if new != parent.body:
                parent_copy.body = new
                return parent_copy.copy()
            else: return parent_copy.copy()
    elif parent.left: return mutation(parent.left)
    elif parent.right: return mutation(parent.right)
    else: return parent.copy()

    
def random_subtree(parent2):
    rand = random.uniform(0,1)
    if rand > CROSSOVER_RATE or (not parent2.left and not parent2.right): 
        return parent2.copy()
    elif parent2.left: return random_subtree(parent2.left)
    elif parent2.right: return random_subtree(parent2.right)

def crossover(parent1, parent2):
    if parent1.body in operators:
        rand = random.uniform(0,1)
        if rand > CROSSOVER_RATE or (not parent1.left and not parent1.right): # xo at this node
            parent1_copy = parent1.copy()
            parent2_subtree = random_subtree(parent2)
            parent1_copy.left = parent2_subtree
            return parent1_copy.copy()
        elif parent1.left: return crossover(parent1.left, parent2)
        elif parent1.right: return crossover(parent1.right, parent2) 
    else:
        return parent1.copy()
            
def tree_len(tree):
    if tree is None:
        return 0
    return 1 + tree_len(tree.get_left()) + tree_len(tree.get_right())
        
def init_population(): # ramped half-and-half
    population = []
    for md in range(2, MAX_DEPTH - 1):
        for _ in range(int(POP_SIZE/ 2)):
            t = Tree()
            t.random_tree(grow = True, max_depth = md) # grow
            population.append(t) 
        for _ in range(int(POP_SIZE/ 2)):
            t = Tree()
            t.random_tree(grow = False, max_depth = md) # full
            population.append(t) 
    return population

def main():
    t1 = Tree()
    t1.random_tree(grow = True, max_depth = MAX_DEPTH, depth = 0)
    
    t1.print_tree()
    print(t1.compute_tree(1))

if __name__ == "__main__":
    main()
