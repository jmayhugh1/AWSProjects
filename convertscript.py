import json
'''
This is meant to read in a script file and convert into a comma seperated array
that can be used in an AWS SSMDocument
'''
#read in name from user
name = input("Enter the name of the file you want to read in: ")
#reads in from a file and converts each line to a list of strings by seperating each memebr at the new lines

with open(name, 'r') as f:
    instances = f.read().splitlines()
print(instances)

# read in json file
jsonname = input("Enter the name of the json file you want to read in: ")
with open(jsonname, 'r') as f:
    jsonfile = json.load(f)
print(jsonfile["mainSteps"])
#loop through until you find inputs
for i in jsonfile["mainSteps"]:
    if i["inputs"]['runCommand']:
        i["inputs"]['runCommand'] = instances
        print(i["inputs"]['runCommand'])
        break
#write out to a new file
newname = input("Enter the name of the new json file you want to write out to: ")
with open(newname, 'w') as f:
    f.write(json.dumps(jsonfile, indent=4))
   


