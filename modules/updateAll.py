import requests
import json as j
import pandas as pd

from modules.globals import *
from modules import utils

async def run(access_token):
    try:
        # Formulate headers for future requests
        headers = {"Authorization": "Bearer " + access_token}

        # Request data from API using headers + Convert response to JSON
        base = base_url + "beta/users/?$select=id, displayname, proxyAddresses, userPrincipalName, lastPasswordChangeDateTime"
        response = requests.get(base, headers=headers)
        json = j.loads(response.text)

        # Formulate list of api requests to make, then make them. (for user permissions and licenses).
        perm_urls = []
        for Dict in json['value']:
            perm_urls.append(f"{base_url}v1.0/users/{Dict['id']}/transitiveMemberOf")
        perm_results = await utils.async_mass_request(json, perm_urls, headers)

        license_urls = []
        for Dict in json['value']:
            license_urls.append(f"{base_url}v1.0/users/{Dict['id']}/licenseDetails")
        license_results = await utils.async_mass_request(json, license_urls, headers)

        # Removal of unneeded ID
        for Dict in json['value']:
            Dict.pop('id')

        # Append permissions to json
        for Dict, perms in zip(json['value'], perm_results):
            Dict['Permissions'] = [item['displayName'] for item in perms['value']] if perms['value'] else None

        for Dict, test in zip(json['value'], license_results):
            Dict['Licenses'] = [item['skuPartNumber'] for item in test['value']] if test['value'] else None

        # Replace all '[]' with None
        for Dict in json['value']:
            for key, value in Dict.items():
                if value == []:
                    Dict[key] = None

        # Remove list formatting for single items
        for Dict in json['value']:
            for key, value in Dict.items():
                if isinstance(value, list) and len(value) == 1:
                    Dict[key] = value[0]

        # Turn lists into value + value
        for Dict in json['value']:
            for key, value in Dict.items():
                if isinstance(value, list):
                    Dict[key] = ' + '.join(value)

        # Convert JSON to Pandas DataFrame and export to CSV
        moved_cols = ["displayName", "Licenses", "proxyAddresses", "userPrincipalName", "lastPasswordChangeDateTime", "Permissions"]
        renamed_cols = ['Display Name', 'Licenses', 'Proxy Addresses', 'User Principle Name', 'Last Password Change', 'Permissions']
        df = pd.json_normalize(json, record_path = ['value'])
        df = df.reindex(columns=moved_cols)
        df.columns = renamed_cols
        df.to_csv('output.csv', index=False)
        return f'Data has been stored in "output.csv" in the root directory.\nRequested Data: \n{df}'
    
    except Exception as e:
        return e