import os
import requests
from dotenv import load_dotenv

load_dotenv()
apiID = (os.environ.get('apiID'))
apiKEY = (os.environ.get('apiKEY'))

# Prep the API url for requests
baseURL = "https://api.dome9.com/v2/Compliance/Ruleset"

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