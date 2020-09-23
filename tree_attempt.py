import operator
import random
import copy

MIN_DEPTH = 2    # minimal initial random tree depth
MAX_DEPTH = 2    # maximal initial random tree depth

def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
operators = [add, sub, mul]
#operators = [('+', operator.add), ('-', operator.sub), ('*', operator.mul), ('/', operator.truediv)]
terminals = [-2, -1, 1, 2, 'x']

class Tree:
    def __init__(self, body = None, left = None, right = None):
        self.body  = body
        self.left  = left
        self.right = right

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
                if random.random() > 0.5:
                    self.body = random.choice(terminals)
                else:
                    self.body = random.choice(operators)
            if self.body in operators:
                self.left = Tree()
                self.left.random_tree(grow, max_depth, depth = depth + 1)
                self.right = Tree()
                self.right.random_tree(grow, max_depth, depth = depth + 1)

    def copy(self):
      
        return copy.deepcopy(self)

def main():
        t = Tree()
        t.random_tree(grow = True, max_depth = MAX_DEPTH, depth = 0)
        t.print_tree()

if __name__ == "__main__":
    main()
