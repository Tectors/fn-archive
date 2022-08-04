#!/usr/bin/python3

from requests import get
import base64

# Gets the splash for the game
def get_splash(version, type="mobileBgImg"):
    v_end = get('https://www.epicgames.com/fortnite/en-US/api/cms/home').json()['pageClasses'].split('ch').pop().split('s')

    # The endpoint
    endpoint = 'https://www.epicgames.com/fortnite/en-US/api/cms/home-{0}'

    # Parse the version into correct numbers (ex: 17 to 27)
    version = [v_end[0], v_end[1]]

    # The short-hand id
    id = 'ch{0}s{1}'.format(version[0], str(int(version[1]) + 1))

    print(id)

    # Request the api with the id and type
    buffer = get(get(endpoint.format(id)).json()['carousel']['slides'][0]['background']['desktopImage']).content

    # Encode and return it
    return 'data:image/png;base64,' + str(base64.b64encode(buffer)).split('\'')[1].split('\'')[0]
