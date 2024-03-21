#!/usr/bin/python3

# NOTE: This is the imports for the file,
# NOTE: there is a bunch of modules being imported,
# NOTE: that are made for this file.

# NOTE: The manifest module is used to make make the manifests
import modules.manifest as manifest_module

from requests import get
from os import path

# Global functions used
from modules.global_functions import parse_build_version

# NOTE: 1. Commences the manifest module

mappings = get('https://fortnitecentral.genxgames.gg/api/v1/mappings').json()

# Parsing the build version will give us more information about the update
parsed = parse_build_version(mappings[0]["fileName"])

update = path.exists("./.github/source/dependents/gen." + parsed['version'] + ".svg")
text = ""

if update:
    text = "Revise "
else:
    text = "Add "

import os
env_file = os.getenv('GITHUB_ENV')

manifests = manifest_module.commence_fest()['response']

if not path.exists('./manifests/' + manifests[-1]['name']):
    text = "Add "
    print("hi")

manifest_module.commence_fest_import()

with open(env_file, "a") as myfile:
    myfile.write(f"version_build={text}{parsed['version'] + '-CL-' + parsed['netcl']} manifest\"")