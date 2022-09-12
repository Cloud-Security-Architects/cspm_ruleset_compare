import os
import requests
from dotenv import load_dotenv

load_dotenv()
apiID = (os.environ.get('apiID'))
apiKEY = (os.environ.get('apiKEY'))

# Pulls down a whole mess of shit
r = requests.get('https://api.dome9.com/v2/Compliance/Ruleset/', auth=(apiID, apiKEY))

# gives the mess of shit a bit o'json
bundles = r.json()

# How to use the properties of a data structure
#print(bundles[0].keys())

# Picking out specific items
bundle = bundles[9]

# How to use dict keys to pull values
#print(bundle["name"])

# iterating through to get certain info
#for bundle in bundles:
#    print(bundle["id"], bundle["name"], bundle["description"],sep="\t")

az1 = requests.get('https://api.dome9.com/v2/Compliance/Ruleset/-140', auth=(apiID, apiKEY))
ruleset1 = az1.json()
rules1 = ruleset1["rules"]
for rule in rules1:
    rule["dupe"] = False
    rule["ruleset2Id"] = 0

#for key,value in rules[0].items():
#    print(key,value,sep="\t")

r2 = requests.get('https://api.dome9.com/v2/Compliance/Ruleset/-85', auth=(apiID, apiKEY))
ruleset2 = r2.json()
rules2 = ruleset2["rules"]
for rule in rules2:
    rule["dupe"] = False

# Create new list for duplicated rules
rd = []

for rule in rules1:
    logic1 = rule["logic"]
#    print(logic1)
    for rule2 in rules2:
        if logic1 == rule2["logic"]:
            #print(f"{ruleset2['name']} Rule '{rule2['name']}' is a duplicate of {ruleset1['name']} Rule '{rule['name']}'!")
            rule2["dupe"] = True
            rule["dupe"] = True
            if rule["ruleId"]!= rule2["ruleId"]:
                rule["ruleset2Id"] = rule2["ruleId"]
            rd.append(rule)
print(f"{ruleset1['name']} Unique Rules")
for rule in rules1:
    if not rule["dupe"]:
        print(f"\t{rule['ruleId']}\t{rule['name']}")
print(f"{ruleset2['name']} Unique Rules")
for rule in rules2:
    if not rule["dupe"]:
        print(f"\t{rule['ruleId']}\t{rule['name']}")
print(f"Rules Common to both {ruleset1['name']} and {ruleset2['name']}")
for rule in rd:
    if rule['ruleset2Id'] != 0:
        print(f"\t{rule['ruleId']}:{rule['ruleset2Id']}\t{rule['name']}")
    else:
        print(f"\t{rule['ruleId']}\t{rule['name']}")