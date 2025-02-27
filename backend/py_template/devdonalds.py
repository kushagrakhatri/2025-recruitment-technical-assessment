from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify, Response
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = list()
cookbook_names = list()

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	# TODO: implement me

	if recipeName == "":
		return None


	recipeName = recipeName.replace("-", " ").replace("_", " ")
	words = list()
	for word in recipeName.split():
		word = "".join(c for c in word if c.isalpha())  # keep only valid letters
		word = word.title()
		words.append(word)
		
	return " ".join(words)


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	# TODO: implement me

	data = request.get_json()
	print(cookbook)

	type = data.get('type', '')
	entry = CookbookEntry(data.get('name', ''))
	cookTime = data.get('cookTime', '')
	requiredItems = data.get('requiredItems', '')

	
	if type is None or entry is None:
		return "asd", 400
	
	if entry.name in cookbook_names:
		return 'ewr', 400
	else:
		cookbook_names.append(entry.name)


	items = list()
	if type == "recipe":
		recipe = Recipe(entry, list())
		item_names = list()
		for item in requiredItems:
			name = item['name']
			quantity = int(item['quantity'])
			if name not in item_names:
				item_names.append(name)
				recipe.required_items.append(RequiredItem(name, quantity))
			else:
				return "ksjdf", 400

		if recipe not in cookbook:
			cookbook.append(recipe)
			return '', 200

	if type == "ingredient":
		ingredient = Ingredient(entry, cookTime)
		if ingredient.cook_time < 0:
			return "", 400
		
		if ingredient not in cookbook:
			cookbook.append(ingredient)
			return '', 200

	return 'not implemented', 500


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
