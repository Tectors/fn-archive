#!/usr/bin/python3

# NOTE: This script imports necessary modules and processes Fortnite mappings.

# Import the manifest module
import modules.manifest as manifest_module
from requests import get
from os import path, getenv

# Global functions used
from modules.global_functions import parse_build_version

# Fetch mappings from the API
mappings = get('https://fortnitecentral.genxgames.gg/api/v1/mappings').json()

# Parse the build version to extract more information about the update
parsed = parse_build_version(mappings[0]["fileName"])

# Check if the generated SVG file already exists
update = path.exists(f"./.github/source/dependents/gen.{parsed['version']}.svg")
text = ("Revise" if update else "Add") + " "

# Get the environment file for GitHub actions
env_file = getenv('GITHUB_ENV')

# Fetch manifests and check if the latest manifest file exists
manifests = manifest_module.commence_fest()['response']

if not path.exists(f'./manifests/{manifests[-1]["name"]}'):
    text = "Add "

# Import the manifest
manifest_module.commence_fest_import()

# Write the version build information to the environment file
with open(env_file, "a") as myfile:
    myfile.write(f"version_build={text}{parsed['version']}-CL-{parsed['netcl']} manifest\"\n")