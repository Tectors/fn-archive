#!/usr/bin/python3

# Global functions used
from requests import get
import os.path
import base64
import time

def parse_build_version(BuildVersion) -> str:
    platform = BuildVersion.split('-')[-1]
    type = BuildVersion.split('-')[0]
    version = BuildVersion.split('-')[1]
    netcl  = BuildVersion.split('-')[3]

    return {
        "platform": platform,
        "type": type,
        "version": version,
        "netcl": netcl,
    }

def add_pak_content(pak):
    listing = []

    full_template = open('./source/dependents/templates/definition.svg', 'r').read()

    try:
        for file in reversed(get('https://fortnite-api.com/v2/cosmetics/br/search/all?dynamicPakId={0}'.format(pak)).json()['data']):
            # If the svg already exists
            if (os.path.exists('./source/dependents/referred/' + file['id'] + '.svg')):
                listing.append(file['id'])
                continue
            
            print('Added new SVG with the id: {0}'.format(file['id']))
            time.sleep(2)

            response = get(file['images']['icon'])

            content = full_template
            print('Response on #{0} pak (#{1})'.format(pak, file['id']))

            content = content.replace('{0}', 'data:image/png;base64,' + base64.b64encode(response.content).decode('ascii'))

            with open('./source/dependents/referred/' + file['id'] + '.svg', "w", encoding="utf-8") as f:
                f.write(content)
                listing.append(file['id'])
    except Exception as e:
        print('Error on {0}: {1}'.format(pak, e.__str__()))

        return listing

    return listing

def save_image(content, name):
    with open('./source/dependents/monthly-rotaton/' + name, "wb") as f:
        f.write(content)
    
    return name
