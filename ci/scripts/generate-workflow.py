import yaml
import json
import sys

with open(sys.argv[1], 'r') as f:
    config = yaml.safe_load(f)

jobs = []
lang = config['project']['language']
features = config['project'].get('features', {})

if features.get('lint'):
    jobs.append({"name": "Lint", "template": "common"})
if features.get('test'):
    jobs.append({"name": "Test", "template": f"{lang}"})
if features.get('security_scan'):
    jobs.append({"name": "Security Scan", "template": "common"})
jobs.append({"name": "Build", "template": f"{lang}"})
jobs.append({"name": "Deploy", "template": "common"})

print(json.dumps({"jobs": jobs}))
