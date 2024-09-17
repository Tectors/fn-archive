#!/usr/bin/python3

from requests import post

def get_token():
    try:
        authorization_endpoint = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        # (https://github.com/MixV2/EpicResearch/blob/master/docs/auth/auth_clients.md)
        authorization_token = "MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="

        response = (post(authorization_endpoint, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'basic ' + authorization_token
        }, data={
            'grant_type': 'client_credentials',
            'token_type': 'eg1'
        })).json()

        auth = response['token_type'] + ' ' + response['access_token']

        return auth
    except:
        return False