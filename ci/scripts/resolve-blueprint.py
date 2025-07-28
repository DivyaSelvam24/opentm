import yaml
import sys

with open(sys.argv[1], 'r') as f:
    config = yaml.safe_load(f)

includes = []

lang = config['project']['language']
build_type = config['project']['build_type']
deploy_type = config['project']['deployment']

includes.append(f"- local: templates/{lang}/build.yml")

if config['project'].get('lint'):
    includes.append("- local: templates/common/lint.yml")

if config['project'].get('test'):
    includes.append("- local: templates/common/test.yml")

if config['project'].get('security_scan'):
    includes.append("- local: templates/common/security-scan.yml")

includes.append("- local: templates/common/deploy.yml")

with open('.ci-include.yml', 'w') as out:
    out.write("include:\n")
    for i in includes:
        out.write(f"  {i}\n")
