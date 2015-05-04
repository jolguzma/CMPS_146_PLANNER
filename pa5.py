import json
from collections import namedtuple

from math import sqrt
import pa5_queve
with open('Crafting.json') as f:
	Crafting = json.load(f)

class Queve:

	def __init__(self):
		print "calling initialize "
		self.elements = []

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))

	def get(self):
		return heapq.heappop(self.elements)[1]

# returns the initial state of the search

def make_initial_state(inventory):
	state = inventory
	return state

# set initial state as defined by the imported json file 
intitial_state = make_initial_state(Crafting['Initial'])

def make_goal_checker(goal):
	print goal


	def is_goal(state):

		return True

	return is_goal

is_goal = make_goal_checker(Crafting['Goal'])

def inventory_to_tuple(inventory):
	return tuple(inventory.get(name,0) for i,name in enumerate(Items))

def inventory_to_frozenset(inventory):
	return frozenset(inventory.items())


# creates a list of consumed items and a list
# of required items to create that specific item
# if any
def make_checker(rule):
	# consumed = ""
	# required = ""

	consumes = {}
	required = {}
    
    # stores any items that are consumed 
	if "Consumes" in rule:
		consumes = rule['Consumes']

			 
	# stores any required items 
	if "Requires" in rule:
		required =  rule['Requires']

	# checks if the state satisfies the necessary items that are 
	# consumed and checks if there is a required item that it is
	# present as well, if these cases are satisifed it returns true
	# else false
	def check(state):

		for name in required:
			if name not in state:
				return False

		for name,quantity in consumes.items():
			if name in state:
				if quantity > state[name]:
					return False
			else:
				return False

		return True


	return check


def make_effector(rule):
	consumes = {}
	produces = {}
    
    # stores any items that are consumed 
	if "Consumes" in rule:
		consumes = rule['Consumes']

			 
	# stores any required items 
	produces =  rule['Produces']

	# returns state that is produced after applying the changes of items
	# consumed and adding the newly  produced item if any 
	def effect(state):
		# next_state = update_inventory(state, consumes,produces)

		return update_inventory(state, consumes,produces)

	return effect

def update_inventory(state, rem_inventory, add_inventory):
	next_state = state
	
	for name,quantity in rem_inventory.items():
		next_state[name] =  next_state[name] - quantity
		
		if next_state[name] == 0:
			next_state.pop(name,None)

	next_state.update(add_inventory)
	return next_state


# uses dikstra
def search(graph, initial, is_goal, limit, heuristic):
	plan = {}
	visited_states = []
	prev = {}
	total_cost = {}
	queve = Queve()

	start_state_h = inventory_to_tuple(initial)

	# stores the initial cost and any possible previous state
	prev[start_state_h] = 0
	total_cost[start_state_h] = 0

	while not queve.empty():

		current_state_h = queve.get()
		current_state_f = inventory_to_frozenset(current_state_h)


		# if is_goal(current_state_f):
		# 	print "reached goal!! "
		# 	break

		# returns a list of possible states 
		possible_states =  graph(current_state_f)

		for v in possible_states:

			alt = cost[current_state_h] +  heuristic(v)
			v_h = inventory_to_tuple(v)
			if v_h not in cost or alt < cost[v_h]:
				priority = cost + heuristic(v)
				prev[v_h] = current_state_f
				cost[v_h] = alt
				queve.put(v_h,priority)




	return total_cost, plan


def graph(state):
	print "in graph"
	for r in all_recipes:
		print r.check(state)
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)

def heuristic(next_state):
	return 0

def main():
	# state_dict = {'coal': 5, 'stick': 3}
	# state_dict = {}
	# state_dict = {'cobble': 3} 
	# state_dict.update( {'bench': 3} )
	# state_dict.update( {'stick': 3} )
	# generated_list = graph(state_dict)
	# for n in generated_list:
	# 	print " printing list: ", n
	search(graph, intitial_state,is_goal,1000,heuristic)





if __name__ ==  '__main__':
	import sys
	Items = Crafting['Items']
	# loads Recipe info and then calls the main function to start the program
	Recipe = namedtuple('Recipe',['name','check','effect','cost'])
	all_recipes = []
	for name, rule in Crafting['Recipes'].items():
		checker = make_checker(rule)
		effector = make_effector(rule)
		recipe = Recipe(name, checker, effector, rule['Time'])
		all_recipes.append(recipe)
	main()






