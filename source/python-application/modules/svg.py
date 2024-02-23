#!/usr/bin/python3

def get_badge(TYPE="DEFAULT"):
    return open('source/dependents/badges/LATEST.svg', 'r').read() if TYPE == 'DEFAULT' else open('source/dependents/badges/BRANCH.svg', 'r').read() if TYPE == 'BRANCH' else open('source/dependents/badges/START.svg', 'r').read() if TYPE == 'STARTING_POINT' else '\n'

def determine_badge(verison):
    return get_badge('STARTING_POINT') if verison.split('.')[1] == '00' else get_badge('BRANCH') if verison.split('.')[1] != '00' else '\n' 

def generate(template, parsed_build, splash, release_date):
    # And add the branch part to the svg if it's not the first version of the season
    svg = template.replace('{0}', parsed_build['version'] + '\n                        <!-- {ORG_REPLACEMENT_START} -->\n' + get_badge()
    + '\n                        <!-- Replacement (for branch icon ect..)\n                        {REPLACEMENT_START}\n' + determine_badge(parsed_build['version']).replace('/', '//') + '\n                        {REPLACEMENT_STOP}\n                        -->')

    svg = svg.replace('{3}', parsed_build['version'])
    svg = svg.replace('{4}', splash)
    svg = svg.replace('{1}', 'Release Date')
    svg = svg.replace('{2}', release_date)

    with open('./source/dependents/' + 'gen.' + parsed_build['version'] + '.svg', "w", encoding="utf-8") as f:
        f.write(svg)
