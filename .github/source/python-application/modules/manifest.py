#!/usr/bin/python3

from requests import post, get
from os import path, makedirs

import glob

# The get token function
from modules.token_gen import get_token

######

# Get a new token
authorization = get_token()

# The endpoint that returns information about the manifest
manifest_endpoint = "https://launcher-public-service-prod.ol.epicgames.com/launcher/api/public/assets/v2/platform/{0}/namespace/fn/catalogItem/4fe75bbc5a674f4f9b356b5c90567da5/app/Fortnite/label/Live"
andriod_endpoint = "https://launcher-public-service-prod-m.ol.epicgames.com/launcher/api/public/assets/{0}/5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds?label=Live"

# The download site we want to download from
manifest_route = 'epicgames-download1.akamaized.net'

def commence_fest():
    manifest_response = ((post(manifest_endpoint.format('Windows'), headers={ 'Authorization': authorization })).json())['elements'][0]

    def get_manifest(queries):
        # OVERRIDE FOR ANDRIOD
        if 'labelName' in queries:
            return queries['items']['MANIFEST']['distribution'] + queries['items']['MANIFEST']['path'] + '?' + queries['items']['MANIFEST']['signature']

        uri = queries['uri']
        queryParams = queries['queryParams']

        if queryParams[0]:
            uri += '?'

            for index, param in enumerate(queryParams):
                uri += ('&' if index != 0 else '') + param['name'] + '=' + param['value']

        # And get it
        return uri

    manifests = []
    andriod_manifest = (get('https://launcher-public-service-prod-m.ol.epicgames.com/launcher/api/public/assets/Android/5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds?label=Live', headers={ 'Authorization': authorization })).json()

    # Add the andriod manifest to the list
    manifests.append({
        'labelName': andriod_manifest['labelName'],
        'hash': andriod_manifest['items']['MANIFEST']['hash'],
        'name': andriod_manifest['items']['MANIFEST']['path'].split('/')[-1].split('.manifest')[0],
    })

    directory = './manifests/'

    with open(directory + andriod_manifest['items']['MANIFEST']['path'].split('/')[-1], "w", encoding="utf-8") as f:
        f.write(get(andriod_manifest['items']['MANIFEST']['distribution'] + andriod_manifest['items']['MANIFEST']['path'] + '?' + andriod_manifest['items']['MANIFEST']['signature']).text)

    # For each manifest
    for manifest in manifest_response['manifests']:
        # The url to the download
        route = get_manifest(manifest)

        # The sub-domain
        sub_domain = route.split('https://')[1].split('/')[0]

        # The manifest's name
        name = manifest['items']['MANIFEST']['path'].split('/')[-1] if 'appName' in manifest else manifest['uri'].split('/')[-1]
        manifest_response['globalName'] = name

        # Print the route's main route
        print('Found sub domain route {0}'.format(sub_domain))

        # Check if it's the same route (ex: download.epicgames.com)
        if sub_domain != manifest_route:
            continue

        manifests.append({
            'labelName': manifest_response['labelName'],
            'name': name,
            'hash': manifest_response['hash'],
        })

        if((".\\manifests\\" + name) not in glob.glob(r'.\manifests\*.manifest')):
            if not path.exists(directory + name):
                content = get(route, timeout=1)

                try:
                    # If the directory does not exist, make the directories and it's self leading up to the root
                    if (not path.exists(directory)):
                        print('Created new directory {0}'.format(directory))
                        makedirs(directory)

                    with open(directory + name, "w", encoding="utf-8") as f:
                        f.write(content.text)

                    print(f"({name.split('.')[0]}): Wrote manifest file")

                except Exception:
                    print('Manifest {0} failed with message "{1}"'.format(name, content.text.split('><Message>')[1].split('<')[0]))
                    continue

    # Return the information
    return {
        "response": manifests,
        "name": name
    }
