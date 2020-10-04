import operator
import random
import copy

POP_SIZE = 10   # population size
MIN_DEPTH = 2    # minimal initial random tree depth
MAX_DEPTH = 4   # maximal initial random tree depth
PROB_MUTATION = 0.75  # probability of perfoming a mutation
CROSSOVER_RATE = 0.8  # crossover rate

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
        # self.count = count(self)

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
                return float("inf")
        elif self.body == 'x': return x
        else: return self.body
        
    def mutation(self):
        rand = random.uniform(0,1)
        if rand > PROB_MUTATION or (not self.left and not self.right): # mutate at this node
            if self.body in operators:
                new = random.choice(operators)
                if new != self.body:
                    self.body = new
            else: 
                new = random.choice(terminals)
                if new != self.body:
                    self.body = new
        elif self.left: self.left.mutation()
        elif self.right: self.right.mutation()

        
    # def size(self): # tree size in nodes
    #     if self.body in operators: return 1
    #     l = self.left.size()  if self.left  else 0
    #     r = self.right.size() if self.right else 0
    #     return 1 + l + r

    # def build_subtree(self): # count is list in order to pass "by reference"
    #     t = Tree()
    #     t.body = self.body
    #     if self.left:  t.left  = self.left.build_subtree()
    #     if self.right: t.right = self.right.build_subtree()
    #     return t
                        
    # def scan_tree(self, count, second): # note: count is list, so it's passed "by reference"
    #     count[0] -= 1
    #     if count[0] <= 1:
    #         if not second: # return subtree rooted here
    #             return self.build_subtree()
    #         else: # glue subtree here
    #             self.body  = second.body
    #             self.left  = second.left
    #             self.right = second.right
    #     else:
    #         ret = None
    #         if self.left  and count[0] > 1: ret = self.left.scan_tree(count, second)
    #         if self.right and count[0] > 1: ret = self.right.scan_tree(count, second)
    #         return ret

    # def crossover(self, other): # xo 2 trees at random nodes
    #     if random.random() < CROSSOVER_RATE:
    #         second = other.scan_tree([random.randint(1, other.size())], None) # 2nd random subtree
    #         self.scan_tree([random.randint(1, self.size())], second) # 2nd subtree "glued" inside 1st tree
    #     else :
    #         print("no crossover")


def init_population(): # ramped half-and-half
    population = []
    for md in range(MIN_DEPTH, MAX_DEPTH - 1):
        for i in range(int(POP_SIZE/ 2)):
            t = Tree()
            t.random_tree(grow = True, max_depth = md) # grow
            population.append(t) 
        for i in range(int(POP_SIZE/ 2)):
            t = Tree()
            t.random_tree(grow = False, max_depth = md) # full
            population.append(t) 
    return population

# def count(tree): # counts the number of nodes in tree
#     if not tree: return 0
#     return count(tree.left) + 1 + count(tree.right)

# # function to get the random node
# def get_random_node(tree):
#     a = tree.count
#     b = tree.left.count if tree.left else 0
#     c = tree.right.count if tree.right else 0
    
#     if b == c == 0:
#         return tree.body
    
#     rand_num = random.randint(1, a)
    
#     if rand_num <= b: return get_random_node(tree.left)
#     elif rand_num == b + 1: return tree.val
#     else: return get_random_node(tree.right)


        
def main():
    t1 = Tree()
    t1.random_tree(grow = True, max_depth = MAX_DEPTH, depth = 0)
    t1.print_tree()
    # print(count(t1))
    # print(get_random_node(t1))
    t1.mutation()
    t1.print_tree()

        # print(t1.tree_string())

        # print(t1.compute_tree(3))
        
        # demonstrating mutation
#        t1.mutation()
#
#        t1.print_tree()
#        print(t1.tree_string())
#        print(t1.compute_tree(3))

        # demonstrating crossover
        # t2 = Tree()
        # t2.random_tree(grow = True, max_depth = MAX_DEPTH, depth = 0)
        # t2.print_tree()
        # print(t2.tree_string())
        # print(t2.compute_tree(3))
        
        # t1.crossover(t2)
        
        # t1.print_tree()
        # print(t1.tree_string())
        # print(t1.compute_tree(3))
        
        
        # t2.print_tree()
        # print(t2.tree_string())
        # print(t2.compute_tree(3))
        
        
        
if __name__ == "__main__":
    main()
