"""
Tree Class for dataset1.
Authors: Caroline Sigl and Lindy Bustabad
"""

import operator
import random
import copy

MIN_DEPTH = 2    # minimal initial random tree depth
MAX_DEPTH = 4   # maximal initial random tree depth
PROB_MUTATION = 0.75  # probability of perfoming a mutation at a node
PROB_CROSSOVER = 0.8  # probability of performing a crossover at a node


def add(x, y): return x + y

def sub(x, y): return x - y

def mul(x, y): return x * y

def div(x, y):
    # Protected division
    try:
        return x/y
    except ZeroDivisionError:
        return 0

operators = [add, sub, mul, div]
terminals = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 'x', 'x', 'x', 'x']

class Tree:
    def __init__(self, body=None, left=None, right=None):
        self.body = body
        self.left = left
        self.right = right
        self.fitness = 0

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def __eq__(self, other):
        return self.body == other.body and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.body, self.left, self.right))

    def __str__(self):
        return str(self.body)

    def node_label(self):  
        """
        Returns label for node in tree.
        """
        if (self.body in operators):
            return self.body.__name__
        else:
            return str(self.body)

    def print_tree(self, prefix=""): 
        """
        Prints representation of expression tree to terminal. 
        """
        print("%s%s" % (prefix, self.node_label()))
        if self.left:
            self.left.print_tree(prefix + "   ")
        if self.right:
            self.right.print_tree(prefix + "   ")

    def random_tree(self, grow, max_depth, depth=0):
        """
        Generates random tree using either grow or full methods. 
        """
            # Full method
        if depth < MIN_DEPTH or (depth < MAX_DEPTH and not grow):
            self.body = random.choice(operators)
        elif depth >= MAX_DEPTH:
            self.body = random.choice(terminals)
        else:  # intermediate depth, grow
            if random.random() > 0.9:
                self.body = random.choice(operators)
            else:
                self.body = random.choice(terminals)
        if self.body in operators:
            self.left = Tree()
            self.left.random_tree(grow, max_depth, depth=depth + 1)
            self.right = Tree()
            self.right.random_tree(grow, max_depth, depth=depth + 1)

    def copy(self):
        return copy.deepcopy(self)

    def tree_string(self):
        """
        Returns expression tree as string.
        """
        if self.body is None:
            return 0
        if self.left is None and self.right is None:
            return self.body
        left_sum = self.left.tree_string()
        right_sum = self.right.tree_string()
        if self.body == add:
            return str(left_sum) + '+' + str(right_sum)
        elif self.body == sub:
            return str(left_sum) + '-' + str(right_sum)
        elif self.body == mul:
            return str(left_sum) + '*' + str(right_sum)
        else:
            return str(left_sum) + '/' + str(right_sum)

    def compute_tree(self, x):
        """
        Evaluates tree with passed value of x.
        """
        if (self.body in operators):
            try:
                return self.body(self.left.compute_tree(x), self.right.compute_tree(x))
            except:
                return float("inf")
        elif self.body == 'x': return x
        else: return self.body


def mutation(parent):
    """
    Performs mutation on a selected parent from the population.
    """
    rand = random.uniform(0, 1)
    if rand > PROB_MUTATION or (not parent.left and not parent.right):
        if parent.body in operators:
            parent_copy = parent.copy()
            new = random.choice(operators)
            if new != parent_copy.body:
                parent_copy.body = new
                return parent_copy.copy()
            else:
                return parent_copy.copy()
        else:
            parent_copy = parent.copy()
            new = random.choice(terminals)
            if new != parent.body:
                parent_copy.body = new
                return parent_copy.copy()
            else:
                return parent_copy.copy()
    elif parent.left:
        return mutation(parent.left)
    elif parent.right:
        return mutation(parent.right)
    else:
        return parent.copy()


def random_subtree(parent2, path):
    """
    Selected random subtree from parent2 to cross with parent1.
    """
    rand = random.uniform(0, 1)
    if rand > PROB_CROSSOVER or (not parent2.left and not parent2.right):
        return path
    coin_toss = random.randint(0, 1)
    if not parent2.right or coin_toss % 2 == 1:
        return random_subtree(parent2.left, path+"0")
    return random_subtree(parent2.right, path + "1")


def crossover(parent1, parent2):
    """
    Performs crossover on two parents selected from the population.
    """
    path1 = random_subtree(parent1, "")
    path2 = random_subtree(parent2, "")
    parent1 = parent1.copy()
    parent2 = parent2.copy()
    loc1 = parent1
    loc1parent = parent1
    loc2 = parent2
    loc2parent = parent2
    for i in range(len(path1)):
        loc1parent = loc1
        if path1[i] == "1":
            loc1 = loc1parent.get_right()
        else:
            loc1 = loc1parent.get_left()
    for i in range(len(path2)):
        loc2parent = loc2
        if path2[i] == "1":
            loc2 = loc2parent.get_right()
        else:
            loc2 = loc2parent.get_left()
    if(len(path1)-1 >= 0):
        if path1[len(path1)-1] == "1":
            loc1parent.right = loc2
        else:
            loc1parent.left = loc2
    if(len(path2) - 1 >= 0):
        if path2[-1] == "1":
            loc2parent.right = loc1
        else:
            loc2parent.left = loc1
    return (parent1, parent2)


def tree_depth(tree):
    """
    Returns tree depth.
    """
    if tree is None:
        return 0
    return 1 + max(tree_depth(tree.get_left()), tree_depth(tree.get_right()))


def init_population(pop_size):  
    """
    Initialize population using ramped half-and-half method.
    """
    population = []
    for md in range(2, MAX_DEPTH - 1):
        for _ in range(int(pop_size / 2)):
            t = Tree()
            t.random_tree(grow=True, max_depth=md)  # Grow method 
            population.append(t)
        for _ in range(int(pop_size / 2)):
            t = Tree()
            t.random_tree(grow=False, max_depth=md)  # Full method
            population.append(t)
    return population

