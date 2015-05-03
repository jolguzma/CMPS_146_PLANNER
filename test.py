import json
from collections import namedtuple
with open('Crafting.json') as f:
	Crafting = json.load(f)



# returns the initial state of the search

def make_initial_state(inventory):
	state = 0
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
	
	print "in inventory ", len(Items)
	
	return tuple(inventory.get(name,0) for i,name in enumerate(Items))

def inventory_to_frozenset(inventory):
	return frozenset(inventory.items())


def make_checker(rule):
	# consumed = ""
	# required = ""

	itemsConsumed = {}
	itemsRequired = {}

	if "Consumes" in rule:
		print rule['Consumes']
		for name,quantity in rule['Consumes'].items():
			


			print "item consumed: " , name, "quantity: ", quantity


	if "Requires" in rule:
		print "requires" , rule['Requires']


	def check(state):
		print "returning from checker"
		inventory = inventory_to_frozenset(state)

		return True

	return check




def make_effector(rule):

	def effect(state):
		print "returning from effector"
		return state

	return effect




# uses dikstra
def search(graph, initial, is_goal, limit, heuristic):


	return total_cost, plan


def graph(state):
	for r in all_recipes:
		print r
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)



def heuristic(next_state):
	return 

def main():
	
	dist = {}	
	state = 3
	graph(state)
	state_dict = {'coal': 5}
	h =  inventory_to_tuple(state_dict)





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






