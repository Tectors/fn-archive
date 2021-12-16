#!/usr/bin/python3

from requests import get
import base64

# Gets the splash for the game
def get_splash(version, type="mobileBgImg"):
    # The endpoint
    endpoint = 'https://www.epicgames.com/fortnite/en-US/api/page?slug={0}&type=battle-pass'

    # Parse the version into correct numbers (ex: 17 to 27)
    version = [str(int(list(version.split('.')[0])[0]) + 1), list(version.split('.')[0])[1]]

    if version[0] == '2' and version[1] == '9':
        version[0] = 3
        version[1] = 1

    # The short-hand id
    id = 'chapter-{0}-season-{1}'.format(version[0], version[1])

    print(id)

    # Request the api with the id and type
    buffer = get(get(endpoint.format(id)).json()['data'][id]['header']['blocks'][0]['logo']['mobileImage']).content

    # Encode and return it
    return 'data:image/png;base64,' + str(base64.b64encode(buffer)).split('\'')[1].split('\'')[0]
