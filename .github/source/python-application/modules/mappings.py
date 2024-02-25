from requests import get
from os import path, makedirs

def commence_mappings_fest():
    mappings = get('https://fortnitecentral.genxgames.gg/api/v1/mappings').json()

    directory = './manifests/mappings/'

    for mapping in mappings:
        # The url to the download
        route = mapping['url']

        # The manifest's name
        name = route.split('/')[-1]

        if not path.exists(directory + name):
            content = get(route, timeout=1)

            try:
                # If the directory does not exist, make the directories and it's self leading up to the root
                if (not path.exists(directory)):
                    print('Created new directory {0}'.format(directory))
                    makedirs(directory)

                with open(directory + name, "w", encoding="utf-8") as f:
                    f.write(content.text)

                print(f"({name.split('.usmap')[0]}): Wrote mapping file")

            except Exception:
                print('Mappings {0} failed with message "{1}"'.format(name, content.text.split('><Message>')[1].split('<')[0]))
                continue