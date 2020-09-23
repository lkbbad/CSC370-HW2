import operator
import random


operators = [('+', operator.add), ('-', operator.sub), ('*', operator.mul), ('/', operator.truediv)]
terminals = [-2, -1, 1, 2, 'x']

class Tree:
    def __init__(self, body):
        self.body = body
        self.left = None
        self.right = None
        # flag for operators to distinguish from operands
        self.operator = False

    def __str__(self):
        return str(self.body)

def print_tree(tree):
    if tree == None: return 0
    print_tree(tree.left)
    print(tree.body)
    print_tree(tree.right)

def build_individual():
    individual = Tree(random.choice(operators))

def main():
    build_individual()

if __name__ == "__main__":
    main()
