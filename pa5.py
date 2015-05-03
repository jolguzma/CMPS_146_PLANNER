import json
from collections import namedtuple
with open('Crafting.json') as f:
	Crafting = json.load(f)



# returns the initial state of the search

def make_initial_state(inventory):
	state = inventory
	return state

# set initial state as defined by the imported json file 
intitial_state = make_initial_state(Crafting['Initial'])

def make_goal_checker(goal):

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
		print "checking : item ", consumes
		print "required : item ", required
		print state

		for name,quantity in consumes.items():
			if name in state:
				if quantity == state[name]:
					print "exists "
				else:
					return False
			else:
				 return False
		for name, in required.items():
			if name not in state:
				print "does not meet the required item which is : ", name
				return False

		return True

	return check


def make_effector(rule):

	def effect(state):

		return state

	return effect




# uses dikstra
def search(graph, initial, is_goal, limit, heuristic):


	return total_cost, plan


def graph(state):
	print "in graph"
	for r in all_recipes:
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)
		break

def heuristic(next_state):
	return 

def main():
	# state_dict = {'coal': 5, 'stick': 3}
	state_dict = {}
	state_dict = {'cobble': 3} 
	state_dict.update( {'bench': 3} )
	generated_list = graph(state_dict)
	print generated_list
	for n in generated_list:
		print " printing list: ", n





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






