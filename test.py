from src.aux.utils import DotDict as dd
import json

with open('config.json', 'r') as config_file:
    config_dict = json.load(config_file)
    
config = dd(config_dict)

print(config.scratch.companies)