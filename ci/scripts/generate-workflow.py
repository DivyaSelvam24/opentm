import yaml
import json
import sys

with open(sys.argv[1], 'r') as f:
    config = yaml.safe_load(f)

project = config['project']
lang = project['language']
build_type = project.get('build_type')
deployment = project.get('deployment')
features = project.get('features', {})

jobs = []

# Add linting and testing
if features.get('lint'):
    jobs.append({"name": "Lint", "template": f"{lang}"})

if features.get('test'):
    jobs.append({"name": "Test", "template": f"{lang}"})

if features.get('security_scan'):
    jobs.append({"name": "Security Scan", "template": "common"})

# Add language-specific build step
if build_type:
    jobs.append({"name": "Build", "template": f"{lang}"})

# Add deployment step (Docker, Terraform, etc.)
if deployment:
    jobs.append({"name": "Deploy", "template": deployment.lower()})

print(json.dumps({"jobs": jobs}))
