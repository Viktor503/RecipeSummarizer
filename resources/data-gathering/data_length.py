import json
f = open('resources/data-gathering/data.json', 'r')
data = json.load(f)
#405-streetkitchen
#1045?-tastecom
#2011-all_recipes
print(len(data))