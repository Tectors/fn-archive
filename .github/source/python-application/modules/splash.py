#!/usr/bin/python3

from requests import get
import base64

# Gets the splash for the game
def get_splash(version, type="mobileBgImg"):
    # NOTE: Expected to fail again in the future
    endpoint = 'https://cdn2.unrealengine.com/fortnite-battle-royale-wrecked-social-1920x1080-657551d6cecf.jpg'
    buffer = get(endpoint).content
    
    # Encode and return it
    return 'data:image/png;base64,' + str(base64.b64encode(buffer)).split('\'')[1].split('\'')[0]
