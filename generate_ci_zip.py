from zipfile import ZipFile, ZIP_DEFLATED
import os

# Define the structure and contents of the repository
repo_structure = {
    ".github/workflows/main.yml": """name: CI Pipeline

on:
  push:
    branches: [main, dev, staging]
  pull_request:

jobs:
  generate:
    runs-on: ubuntu-latest
    name: Generate CI Workflow
    outputs:
      matrix: ${{ steps.generate.outputs.matrix }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Generate Workflow Steps from Blueprint
        id: generate
        run: |
          python3 ci/scripts/generate-workflow.py ci/blueprint.yml > ci/generated-jobs.json
          echo "matrix=$(cat ci/generated-jobs.json | jq -c .jobs)" >> $GITHUB_OUTPUT

  run-jobs:
    needs: generate
    runs-on: ubuntu-latest
    strategy:
      matrix: ${{ fromJson(needs.generate.outputs.matrix) }}
    name: ${{ matrix.name }}
    steps:
      - uses: actions/checkout@v4

      - name: Run ${{ matrix.name }}
        uses: ./.github/actions/${{ matrix.template }}
""",
    "ci/blueprint.yml": """project:
  name: example-app
  language: python
  build_type: poetry
  deployment: terraform
  environments: [dev, staging, prod]
  branching_strategy: trunk
  versioning: semver
  features:
    lint: true
    test: true
    security_scan: true
    coverage: true
""",
    "ci/scripts/generate-workflow.py": """import yaml
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
""",
    ".github/actions/lint/action.yml": """name: "Lint Code"
runs:
  using: "composite"
  steps:
    - run: |
        echo "Running linter..."
""",
    ".github/actions/python-test/action.yml": """name: "Python Tests"
runs:
  using: "composite"
  steps:
    - run: |
        pip install -r requirements.txt
        pytest --cov=.
""",
    ".github/actions/python-build/action.yml": """name: "Python Build"
runs:
  using: "composite"
  steps:
    - run: |
        pip install poetry
        poetry install
        poetry build
""",
    ".github/actions/deploy/action.yml": """name: "Deploy"
runs:
  using: "composite"
  steps:
    - run: |
        echo "Deploying with Terraform"
"""
}

# Create zip file
zip_filename = "github-ci-blueprint-framework.zip"

with ZipFile(zip_filename, 'w', ZIP_DEFLATED) as zipf:
    for path, content in repo_structure.items():
        zipf.writestr(path, content)

print(f"Created: {zip_filename}")
