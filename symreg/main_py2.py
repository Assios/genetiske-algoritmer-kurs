#!/usr/bin/env python
# coding: latin1

import math
import random

def mean(arr):
	return sum(arr)/len(arr)

class Operation:
	def __init__(self, name, func):
		self.name = name
		self.func = func

	@property
	def argument_count(self):
		return self.func.__code__.co_argcount

	def call(self, *args):
		vectorize = lambda f: (lambda *arg: [f(*[a[i] for a in arg]) for i in range(len(arg[0]))])
		return vectorize(self.func)(*args)

OPERATIONS = {
	'+': Operation('+', lambda a, b: a + b),
	'*': Operation('*', lambda a, b: a * b),
	'sqrt': Operation('sqrt', lambda a: math.sqrt(abs(a))),
	'abs': Operation('abs', lambda a: abs(a))
}

class Node:
	def __init__(self, operation, variables, children):
		assert operation.argument_count == len(children)
		self.operation = operation
		self.variables = variables
		self.children = children

	def __str__(self):
		if len(self.children) == 1:
			return '{}({})'.format(self.operation.name, str(self.children[0]))
		elif len(self.children) == 2:
			return '({} {} {})'.format(str(self.children[0]), self.operation.name, str(self.children[1]))
		else:
			raise Exception('{}, {}'.format(self.operation.name, self.children))

	def evaluate(self, data):
		return self.operation.call(*[c.evaluate(data) for c in self.children])

class Leaf:
	def __init__(self, variable):
		self.variable = variable

	def __str__(self):
		return self.variable

	def evaluate(self, data):
		return data[self.variable]

def build_leaf(variables, max_depth):
	leaf_probability = 1/max_depth
	return Leaf(random.choice(variables)) if (random.random() < leaf_probability or max_depth == 1) else generate_random_tree(variables, max_depth-1)

def generate_random_tree(variables, max_depth):
	operation_names = list(OPERATIONS.keys())
	operation = OPERATIONS[random.choice(operation_names)]
	return Node(operation, variables, [build_leaf(variables, max_depth) for i in range(operation.argument_count)])

def generate_initial_trees(variables, n, max_depth=4):
	return [generate_random_tree(variables, max_depth) for i in range(n)]

def chunk(li, chunk_count):
    for i in range(0, len(li), int(chunk_count)):
        yield li[i:i + int(chunk_count)]

def calculate_score(y_true, y_pred):
	return mean([abs(y_true[i] - y_pred[i]) for i in range(len(y_true))])

def run_tournament(X, y, trees):
	best_tree = (0, float('inf'))
	for i, tree in enumerate(trees):
		evaluation = tree.evaluate(X)
		score = calculate_score(y, evaluation)
		if score < best_tree[1]:
			best_tree = (i, score)
	print('Best tree: ' + str(trees[best_tree[0]]))
	return trees[best_tree[0]]

def is_complete(X, y, winning_trees, threshold):
	for tree in winning_trees:
		if calculate_score(y, tree.evaluate(X)) < threshold:
			return True
	return False

def copy_between_trees(tree_1, tree_2):
	### TODO: Implementer meg!
	return tree_1

def replace_part_with_random(tree):
	### TODO: Implementer meg!
	return tree

def evolve_trees(start_trees, population_size):
	trees = []
	while len(trees) < population_size:
		random_tree = random.choice(start_trees)
		random_tree_2 = random.choice(start_trees)
		p = random.random()
		if p < 1/3:
			trees.append(generate_random_tree(random_tree.variables, 4))
		elif p < 2/3:
			trees.append(copy_between_trees(random_tree, random_tree_2))
		else:
			trees.append(replace_part_with_random(random_tree))
	return trees

def symreg(X, y, variables, population_size, max_generations, error_threshold):
	trees = generate_initial_trees(variables, population_size) # Lager population_size antall tilfeldige trær
	for i in range(max_generations):
		print('Kjører generasjon ' + str(i))
		tournament_participants = list(chunk(trees, math.floor(population_size/10))) # Deler opp trærne i turneringspuljer
		winners = [run_tournament(X, y, participants) for participants in tournament_participants] # Regner ut vinneren av hver gruppe
		if is_complete(X, y, winners, error_threshold):
			# Sjekker om vi har funnet en løsning som gir mindre feil enn error_threshold
			break
		trees = evolve_trees(winners, population_size) # Muterer og kombinerer vinnerne til nye trær
	return run_tournament(X, y, trees) # Returnerer den beste av løsningene som nå ligger i trees

if __name__ == '__main__':
	# Genererer data for y = x^2 + z
	variables = ['x', 'z']
	X = {'x': [-5 + 0.1*k for k in range(100)], 'z': [3 + 0.2*k for k in range(100)]}
	y = [row[0]*row[0] + row[1] for row in zip(*X.values())]

	# Bygger en symbolsk regresjon-modell
	best_model = symreg(X, y, variables, population_size=1000, max_generations=50, error_threshold=0.1)
	print('{} vant med en feil på {}!'.format(best_model, calculate_score(y, best_model.evaluate(X))))