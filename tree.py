import operator
import random
import copy

POP_SIZE = 1000   # population size
MIN_DEPTH = 2    # minimal initial random tree depth
MAX_DEPTH = 3   # maximal initial random tree depth

def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
def div(x, y): return x / y
operators = [add, sub, mul, div]
terminals = [-2, -1, 1, 2, 'x','x','x']

class Tree:
    def __init__(self, body = None, left = None, right = None):
        self.body  = body
        self.left  = left
        self.right = right
        self.fitness = 0

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

    def random_tree(self, grow, max_depth, depth = 0): # create random tree using either grow or full method
            if depth < MIN_DEPTH or (depth < max_depth and not grow):
                self.body = random.choice(operators)
            elif depth >= max_depth:
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
            return str(left_sum) + '+' + str(right_sum) 
        elif self.body == sub: 
            return str(left_sum) + '-' +  str(right_sum)
        elif self.body == mul: 
            return str(left_sum) + '*' +  str(right_sum) 
        else: 
            return str(left_sum) + '/' +  str(right_sum) 

    def compute_tree(self, x): 
        if (self.body in operators): 
            try:
                return self.body(self.left.compute_tree(x), self.right.compute_tree(x))
            except:
                return None
        elif self.body == 'x': return x
        else: return self.body

def init_population(): # ramped half-and-half
    population = []
    for md in range(3, MAX_DEPTH + 1):
        for i in range(int(POP_SIZE/6)):
            t = Tree()
            t.random_tree(grow = True, max_depth = md) # grow
            population.append(t) 
        for i in range(int(POP_SIZE/6)):
            t = Tree()
            t.random_tree(grow = False, max_depth = md) # full
            population.append(t) 
    return population
        
def main():
        t = Tree()
        t.random_tree(grow = True, max_depth = MAX_DEPTH, depth = 0)
        t.print_tree()
        print(t.tree_string())
        print(t.compute_tree(3))

if __name__ == "__main__":
    main()
