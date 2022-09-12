from ntpath import join
import sys
import os
import requests
from dotenv import load_dotenv
load_dotenv()
apiID = (os.environ.get('apiID'))
apiKEY = (os.environ.get('apiKEY'))

# Prep the API url for requests
baseURL = "https://api.dome9.com/v2/Compliance/Ruleset/"

# Pull all ruleset IDs from tenant
bundles = requests.get('https://api.dome9.com/v2/Compliance/Ruleset/view', auth=(apiID, apiKEY))
bundles = bundles.json()
ridlist = []
for r in bundles:
    ridlist.append(int(r['id']))
print(ridlist)

# Get first ruleset ID
while True:
    try:
        rId1 = int(input("Enter RulesetId of first ruleset to compare: "))
        while rId1 not in ridlist:
            print("That is not a valid Ruleset ID, please try again.")
            rId1 = int(input("Enter RulesetId of first ruleset to compare: "))
    except ValueError:
        print("-_- no")
        continue
    else:
        break

while True:
    try:
        rId2 = int(input("Enter RulesetId of second ruleset to compare: "))
        while rId1 not in ridlist:
            print("Come on. You're better than that. Or are you?")
            rId1 = int(input("Enter RulesetId of second ruleset to compare: "))
    except ValueError:
        print("Just, no.")
        continue
    else:
        break

url1 = ''.join([baseURL, str(rId1)])
url2 = ''.join([baseURL, str(rId2)])

# Pulls down a whole mess of shit
r1 = requests.get(url1, auth=(apiID, apiKEY))
r2 = requests.get(url2, auth=(apiID, apiKEY))

ruleset1 = r1.json()
ruleset2 = r2.json()
r1name = ruleset1['name']
r2name = ruleset2['name']

# Pull the rules out of the bundles
# Create couple of extra fields for tracking
rules1 = ruleset1["rules"]
for rule in rules1:
    rule["dupe"] = False
    rule["ruleset2Id"] = 0

rules2 = ruleset2["rules"]
for rule in rules2:
    rule["dupe"] = False

# Create new list for duplicated rules
rd = []

for rule in rules1:
    logic1 = rule["logic"]
    for rule2 in rules2:
        if logic1 == rule2["logic"]:
            rule2["dupe"] = True
            rule["dupe"] = True
            if rule["ruleId"]!= rule2["ruleId"]:
                rule["ruleset2Id"] = rule2["ruleId"]
            rd.append(rule)

filename = "Comparison of "+r1name+" and "+r2name+".txt"
f = open(filename, 'w')

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