import json
import sys
def main():
    first = json.load(open(sys.argv[1]))
    second = json.load(open(sys.argv[2]))
    mergerated = {}
    for rule in first["rules"]:
        if not any(rule["logic"] == rule_compare["logic"] for rule_compare in second["rules"]):
            mergerated[rule["logic"]] = rule
        else:
            for rule_compare in second["rules"]:
                if rule["logic"] == rule_compare["logic"]:
                    new_rule = rule
                    new_rule["complianceTag"] = rule["complianceTag"] +"|"+ rule_compare["complianceTag"]
                    mergerated[rule["logic"]] = new_rule
    for rule in second["rules"]:
        if not any(rule["logic"] == rule_compare["logic"] for rule_compare in first["rules"]):
            mergerated[rule["logic"]] = rule
        else:
            for rule_compare in second["rules"]:
                if rule["logic"] == rule_compare["logic"]:
                    new_rule = rule
                    new_rule["complianceTag"] = rule["complianceTag"] +"|"+ rule_compare["complianceTag"]
                    mergerated[rule["logic"]] = new_rule
    print(json.dumps(list(mergerated.items()), indent=4))
if __name__ == "__main__":
    main()