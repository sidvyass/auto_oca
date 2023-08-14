import json

with open("example.json", "r") as jsonfile:
    file = json.load(jsonfile)
    print(file)
