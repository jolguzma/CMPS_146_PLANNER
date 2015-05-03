import json
from collections import namedtuple
with open('Crafting.json') as f:
	Crafting = json.load(f)


# List of items that can be in your inventory:
print Crafting['Items']
# example: ['bench', 'cart', ..., 'wood', 'wooden_axe', 'wooden_pickaxe']

# List of items in your initial inventory with amounts:
print Crafting['Initial']
# {'coal': 4, 'plank': 1}

# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
print Crafting['Goal']
# {'stone_pickaxe': 2}

# Dictionary of crafting recipes:
print Crafting['Recipes']['craft stone_pickaxe at bench']
# example:
# {	'Produces': {'stone_pickaxe': 1},
#	'Requires': {'bench': True},
#	'Consumes': {'cobble': 3, 'stick': 2},
#	'Time': 1
# }

Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items:
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)


def make_checker(rule):
 # this code runs once
	  # do something with rule['Consumes'] and rule['Requires']
	def check(state):
		 # this code runs millions of times
		return True # or False
	
	return check

def make_effector(rule):
	 # this code runs once
  # do something with rule['Produces'] and rule['Consumes']
	def effect(state):
		 # this code runs millions of times
		return next_state
	
	return check


def graph(state):
	for r in all_recipes:
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)

def heuristic(state):
	return 0 # or something more accurate

def make_initial_state(inventory):

	return state

initial_state = make_initial_state(Crafting['Initial'])

def make_goal_checker(goal):
 # this code runs once
def is_goal(state):
	 # this code runs millions of times
	return True # or False

	return is_goal