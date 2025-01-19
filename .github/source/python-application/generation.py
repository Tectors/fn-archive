#!/usr/bin/python3

# NOTE: This is the imports for the file,
# NOTE: there is a bunch of modules being imported,
# NOTE: that are made for this file.

# NOTE: The manifest module is used to make make the manifests
import modules.manifest as manifest_module
# NOTE: The splash module is a way to get the icon for the season
import modules.splash as splash_module
import modules.mappings as mappings_module

from requests import get
from os import path, makedirs

# Global functions used
from modules.global_functions import parse_build_version, add_pak_content, save_image
from modules.ordinal import ordinal

# NOTE: This is the function that'll generate svgs for the README
import modules.svg as scaleable_generator

import glob
from datetime import datetime

import json

# NOTE: This file is used as the main exeuction for the generation
# NOTE: 
# NOTE: The actions are done in the order inside of this python file:
# NOTE:
# NOTE: 1. Commences the manifest module
# NOTE: 2. Resets the icon of the last modifed file if it is not a new version (ICON REPLACEMENT)
# NOTE: 3. Commences the generation of the scale-able files for the thumbnail of the README
# NOTE: 4. Adds the scale-able file as the first element of the README
# NOTE: 5. Get's the keys and sorts them numerically
# NOTE: 6. Adds the keys into the README with the items
# NOTE: 7. Writes the README file into tree
# NOTE:
# NOTE: That is basically what it does in a nutshell
# NOTE: Each part is labled if you are needing help

generated_svg_markdown_template = (
    '<picture>\n  <img '
    'src="https://raw.githubusercontent.com/Tectors/fn-archive/master/.github/source/dependents/gen.{version_number}.svg" '
    'width="360" height="155">\n'
    '</picture>\n\n'
    '> <!--- Spacer inbetween version -->\n'
    '\n'
    '> {long_version}\n'
)

# These will make writing mark-down files eaiser
markdown_keys = ''
manifest_readme_string_start = '## *Manifests*\n'
manifest_readme_string = '| Label | `Hash` | `Route` |\n| - | - | - |\n'
mappings_readme_string = "| Label | Compression Method | `.usmap` |\n| - | - | - |\n"

_text = ''

drop_down = '<details>\n  <summary>{0}</summary>\n\n{1}</details>\n\n'

# NOTE: Request keys, sort the keys and store them at a later use
# NOTE: {

mappings = get('https://fortnitecentral.genxgames.gg/api/v1/mappings').json()
chain = get('https://fortnitecentral.genxgames.gg/api/v1/aes').json()

# Parsing the build version will give us more information about the update
parsed = parse_build_version(mappings[0]["fileName"])

file_path = f"./.github/source/dependents/referred/{parsed['version']}.json"

if not path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(chain, indent=4, sort_keys=True))
else:
    with open(file_path, 'r', encoding="utf-8") as f:
        previous_model = json.load(f)

    prev_dynamicKeys = previous_model['dynamicKeys']
    dynamicKeys = chain['dynamicKeys']

    new_elements = [element for element in dynamicKeys if element not in prev_dynamicKeys]
    _text = ' '.join(f'+ {element["name"].split(".")[0]} ({element["size"]["formatted"]})' for element in new_elements)

    # Write the updated chain to the JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(chain, indent=4, sort_keys=True))

update = path.exists(f"./.github/source/dependents/gen.{parsed['version']}.svg")
text = ("Update" if update else "Add") + " "

import os
env_file = os.getenv('GITHUB_ENV')

# Store some information that is obtained from the response
dynamicKeys = []

# NOTE: Since the dynamicKeys array doesn't include the main key, so we have to add it manually
markdown_keys += f'#### *AES Key*\n```\n{chain["mainKey"]}\n```\n\n'
dynamicKeys.append(chain["mainKey"])

editor_preferences = '('

for package in chain['dynamicKeys']:
    key = package['key']

    # Add aes key
    editor_preferences += f"(Value=\"{key}\",Guid=\"{package['guid']}\"),"

    dynamicKeys.append(key)

    # Add each scale-able content of the package
    pak_content = add_pak_content(int(package['name'].split('-')[0].replace('optional', '').replace('pakchunk', '')))

    # The pak-content in a string used for the listing inside of the drop-down
    markdown_content = '  '
    
    for content in pak_content:
        markdown_content += f'<picture><img src="https://raw.githubusercontent.com/Tectors/fn-archive/master/.github/source/dependents/referred/{content}.svg" width="100"></picture> '
    if pak_content.__len__() > 0:
        markdown_content += '\n'

    markdown_keys += drop_down.format(package['name'], f'  <br>\n\n  ```\n  {key}\n  {package["keychain"]}\n  ```\n\n{markdown_content}')

manifest_readme_string_start += f"<details>\n  <summary>Editor Preferences</summary>\n\n> <!--- Spacing that adds ``` markdown -->\n    {editor_preferences.rsplit(',', 1)[0] + ')'}\n</details>\n\n"

# | Variables defined: dynamicKeys, parsed, chain
# NOTE: }
# NOTE: Defining the splash and release date, and also generating the scale-able files for the mark-down file
# NOTE: {

try:
    splash = splash_module.get_splash(parsed['version'])

    # The release data in the datetime object, used to convert
    release_datetime = datetime.today()

    # The date that the update came out
    updated_at = '{dt:%B} {day}, {dt.year}'.format(dt = datetime.today(), day = ordinal(release_datetime.day)).replace('September', 'Sept').replace('October', 'Oct').replace('August', 'Aug').replace('January', 'Jan').replace('February', 'Feb').replace('December', 'Dec').replace('November', 'Nov')
    
    # If already exists, don't do anything
    # NOTE: this completely removes bloated commits
    if not path.exists(f"./.github/source/dependents/gen.{parsed['version']}.svg"):
        # Generate the scale-able file
        scaleable_generator.generate(open('./.github/source/dependents/templates/source.svg', 'r').read(), parsed, splash, updated_at)
except:
    print('Failed to add splash')

# | Variables defined: splash, release_datetime, day, updated_at
# NOTE: }
# NOTE: Commencing the manifest sequence
# NOTE: {

manifests = manifest_module.commence_fest()['response']
manifest_module.commence_fest_import()

added_manifests = []
mappings_module.commence_mappings_fest()

for manifest in manifests:
    # Check if it was previously added
    if manifest in added_manifests:
        continue

    added_manifests.append(manifest)
    manifest_readme_string += '| *{0}* | {2} | [{1}](https://github.com/Tectors/fn-archive/blob/master/manifests/{1}.manifest) |\n'.format(manifest['labelName'], manifest['name'].replace('.manifest', ''), manifest['hash'])

for mapping in mappings:
    mappings_readme_string += f'| *{mapping["meta"]["platform"]}* | {mapping["meta"]["compressionMethod"]} | [{mapping["url"].split("/")[-1]}](https://github.com/Tectors/fn-archive/blob/master/manifests/mappings/{mapping["url"].split("/")[-1]}) |\n'

manifest_readme_string = manifest_readme_string_start + manifest_readme_string

# | Variables defined: manifests
# NOTE: }
# NOTE: Putting a part the real README
# NOTE: {

versioning = f"{parsed['type']}-{parsed['version']}-CL-{parsed['netcl']}-Windows"

# This adds in the thumbnail (scale-able file) into the mark-down file
markdown_content = generated_svg_markdown_template.replace("{version_number}", parsed["version"]).replace("{long_version}", versioning)
markdown_content += '\n' + manifest_readme_string + '\n' + mappings_readme_string + '\n---\n\n' + markdown_keys

# NOTE: }
# NOTE: Writing the file and we will be complete
# NOTE: {

with open('./builds/' + parsed['version'] + '.md', "w", encoding="utf-8") as f:
    # Write it
    print(f'- Wrote mark-down file ({parsed["version"]})')
    f.write(markdown_content)

with open('README.md', "w", encoding="utf-8") as f:
    # Write it
    f.write(open('./.github/source/dependents/templates/reference.md', 'r').read().replace('{PARSED_VERSION}', parsed['version']))

# NOTE: }
# badge_gen_usage was here <-------

if env_file != None:
    with open(env_file, "a") as myfile:
        myfile.write(f"version_build={text}{parsed['version']}-CL-{parsed['netcl']}\" -m \"{_text}\"")