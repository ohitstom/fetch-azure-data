import requests
import json as j
import pandas as pd

from modules.globals import *
from modules import utils

<<<<<<< HEAD
def run(access_token):
=======
async def run(access_token):
>>>>>>> 5e80d19 (2:32)
    try:
        # Formulate headers for future requests
        headers = {"Authorization": "Bearer " + access_token}

        # Request data from API using headers + Convert response to JSON
        base = base_url + "beta/users/?$select=id, displayname, mail, lastPasswordChangeDateTime"
        response = requests.get(base, headers=headers)
        json = j.loads(response.text)
        
        # Formulate list of api requests to make, then make them. (for user permissions).
        perm_urls = []
        for Dict in json['value']:
            perm_urls.append(f"{base_url}v1.0/users/{Dict['id']}/transitiveMemberOf")
<<<<<<< HEAD
        results = utils.async_mass_request(json, perm_urls, headers)
=======
        results = await utils.async_mass_request(json, perm_urls, headers)
>>>>>>> 5e80d19 (2:32)
        
        # Append permissions to json
        for Dict, perms in zip(json['value'], results):
            Dict['Permissions'] = [item['displayName'] for item in perms['value']] if perms['value'] else None

        # Convert JSON to Pandas DataFrame and export to CSV
        df = pd.json_normalize(json, record_path = ['value'])
        df.to_csv('output.csv')
        return f'Data has been stored in "output.csv" in the root directory.\nRequested Data: \n{df}'
    
    except Exception as e:
        return e