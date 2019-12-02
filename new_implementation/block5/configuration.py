# ToDo: copyright etc
import json

with open('configuration.json', 'r') as f:
    cfg = json.load(f)

if __name__ == '__main__':
    # Just print the configuration dictionary and exit
    import pprint
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(cfg)