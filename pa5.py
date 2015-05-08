import json
import heapq
import copy
from collections import namedtuple

from math import sqrt
with open('Crafting.json') as f:
	Crafting = json.load(f)

class Queve:

	def __init__(self):
		self.elements = []

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))

	def get(self):
		return heapq.heappop(self.elements)[1]

def make_item_list(crafting_items):
	index_of_items = {}
	count = 0
	for item in crafting_items:

		index_of_items[item] = count
		count += 1
	return index_of_items

item_index = make_item_list( Crafting['Items'])


def make_limited_item_list(crafting_items):
	index_of_items = {}
	count = 0
	for item in crafting_items:
		if item == 'bench' or item == 'furnace' or item == 'iron_pickaxe' or item == 'stone_pickaxe' or item == 'wooden_pickaxe' or item == 'wooden_axe' or item == 'iron_axe' or item == 'stone_axe' or item == 'cart':
			index_of_items[item] = count
			count += 1
	return index_of_items


limited_items = make_limited_item_list(Crafting['Items'])

def make_initial_state(inventory):
	state = inventory
	return state

# set initial state as defined by the imported json file 
intitial_state = make_initial_state(Crafting['Initial'])

def make_goal_checker(goal):

	def is_goal(state):

		for thing in goal:
			if thing in state:
				if state[thing] < goal[thing]:
					return False
			else:
				return False

		return True

	return is_goal

is_goal = make_goal_checker(Crafting['Goal'])

def inventory_to_tuple(inventory):
	return tuple(inventory.get(name,0) for i,name in enumerate(Items))

def inventory_to_frozenset(inventory):
	return frozenset(inventory.items())
	
def tuple_to_inventory(tuple):
	inventory = {}
	
def tuple_to_inventory(t):
	inventory = {}
	for i, name in enumerate(Items):
		if t[i] != 0:
			inventory[name] = t[i]
	return inventory
	


# creates a list of consumed items and a list
# of required items to create that specific item
# if any
def make_checker(rule):

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
		next_state = update_inventory(state, consumes,produces)

		return next_state

	return effect

# updates inventory by removing the specified inventory and adding
# the specified inventory
def update_inventory(state, rem_inventory, add_inventory):
	next_state = copy.deepcopy(state)
	
	for name,quantity in rem_inventory.items():
		next_state[name] =  next_state[name] - quantity
		
		if next_state[name] == 0:
			next_state.pop(name,None)

	for name,quantity in add_inventory.items():
		if name not in next_state:
			next_state.update(add_inventory)
		else:
			next_state[name] =  next_state[name] +  quantity
	return next_state


# uses dikstra
def search(graph, initial, is_goal, limit, heuristic):

#for each goal item I have, subtract that off of my goal???

	plan = {}
	visited_states = []
	prev = {}
	total_cost = {}
	queve = Queve()
	start_state_h = inventory_to_tuple(initial)
	found = False
	# stores the initial cost and any possible previous state
	prev[start_state_h] = None
	total_cost[start_state_h] = 0
	queve.put(initial,0)

	if is_goal(initial):
		found = True
		return total_cost[start_state_h],plan,found

	while not queve.empty() and limit > 0:
		#print limit
		limit -= 1

		current_state = queve.get()
		current_state_t = inventory_to_tuple(current_state)
		#print "\ncurrent state" , current_state


		if is_goal(current_state):
			found = True
			break

		# returns a list of possible states 
		possible_states =  graph(current_state)

		for v_name,v_state,v_cost in possible_states:
			#print "possible state:", v_name
			alt = total_cost[current_state_t] + v_cost + heuristic(v_state)
			v_t = inventory_to_tuple(v_state)
			if v_t not in total_cost or alt < total_cost[v_t]:
				priority = alt + heuristic(v_state)
				prev[v_t] = current_state_t
				total_cost[v_t] = alt
				queve.put(v_state,priority)
				if is_goal(v_t):
					found = True
					return total_cost[v_t], traceback(prev, v_t, initial),found

	return total_cost[current_state_t], traceback(prev, current_state_t, initial),found

def traceback(prev, cell, source):
	path = []
	while cell != None:
		path.append(cell)
		cell = prev[cell]
	return path
	
def graph(state):
	# next_state = state
	# possible_states = []

	for r in all_recipes:
		if r.check(state):
			next_state = r.effect(state)
			#print "next state ",  next_state

			yield (r.name, next_state, r.cost)

def heuristic(next_state):
	for item, quantity in next_state.items():
		if item in limited_items  and quantity > 1:
			return sys.maxint - 10
		if item == "stick"	and quantity > 6:
			return sys.maxint - 10
		if item == "plank"	and quantity > 6:
			return sys.maxint - 10
		if item == "wood"	and quantity > 1:
			return sys.maxint - 10
		if item == "coal"	and quantity > 1:
			return sys.maxint - 10
		if item == "ore"	and quantity > 1:
			return sys.maxint - 10
		if item == "cobble"	and quantity > 9:
			return sys.maxint - 10
		if item == "bench" and quantity > 2:
			return sys.maxint - 10

	return 0

def main():
	total_cost, plan, found= search(graph, intitial_state,is_goal,10000,heuristic)
	print 
	
	# if there was a plan found and initial state had nothing 
	if intitial_state == {} and found:
		print "Achieve ", Crafting['Goal'], "from scratch. [cost=",total_cost,", len=",len(plan),"]"
	# if there was not plan found then found will be False 
	elif not found:
		print "Achieving ", Crafting['Goal'], "was not possible from ", intitial_state
	# if there was a given initial state that is no empty (not yet impleented), then 
	else:
		print "Given ", intitial_state, " achieve ", Crafting['Goal'], "[cost=", total_cost, " len=",len(plan), "]"

	print 
	
	if len(plan) > 0:

		for step in reversed(plan):
			print tuple_to_inventory(step), "\n"
	elif found:
		print "Satisifed by initial state"





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