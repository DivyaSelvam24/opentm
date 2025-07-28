import yaml
import json
import sys

with open(sys.argv[1], 'r') as f:
    config = yaml.safe_load(f)

jobs = []
lang = config['project']['language']
features = config['project'].get('features', {})

if features.get('lint'):
    jobs.append({"name": "Lint", "template": "lint"})
if features.get('test'):
    jobs.append({"name": "Test", "template": f"{lang}-test"})
if features.get('security_scan'):
    jobs.append({"name": "Security Scan", "template": "security-scan"})
jobs.append({"name": "Build", "template": f"{lang}-build"})
jobs.append({"name": "Deploy", "template": "deploy"})

print(json.dumps({"jobs": jobs}))
