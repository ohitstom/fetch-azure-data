import webbrowser
import requests
import msal
from msal import PublicClientApplication
import pandas as pd
import json
import pyperclip
import aiohttp
import asyncio

APPLICATION_ID = "4c8d41bc-0a4d-4985-aa15-8c7be46eb52a"
authority_url = "https://login.microsoftonline.com/ffb75476-0afa-47b0-9b8c-6f97809370fe"
base_url = "https://graph.microsoft.com/"
scopes = ["User.Read", "User.Read.All", "AuditLog.Read.All", "RoleManagement.Read.All", "RoleManagementPolicy.Read.Directory", "Group.Read.All"]

app = PublicClientApplication(
    APPLICATION_ID, 
    authority=authority_url
    )

flow = app.initiate_device_flow(scopes=scopes)
print(flow["message"], '\nThis code has been copied to your clipboard.')
pyperclip.copy(flow["user_code"])
webbrowser.open(flow["verification_uri"])

result = app.acquire_token_by_device_flow(flow)

access_token = result["access_token"]
headers = {"Authorization": "Bearer " + access_token}


base = base_url + "beta/users/?$select=id, displayname, mail, lastPasswordChangeDateTime" # signInActivity -> needs premium license + the user to have Reports Reader
response = requests.get(base, headers=headers)
json = json.loads(response.text)

perm_urls = []
for Dict in json['value']:
    perm_urls.append(f"{base_url}v1.0/users/{Dict['id']}/transitiveMemberOf")


async def request(session, url):
    async with session.get(url, headers=headers) as response:
        perms = await response.json()
        return perms

async def get_perms():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[asyncio.ensure_future(request(session, url)) for url in perm_urls])
        return results

results = asyncio.run(get_perms())
for Dict, perms in zip(json['value'], results):
    Dict['Permissions'] = [item['displayName'] for item in perms['value']]

df = pd.json_normalize(json, record_path =['value'])
df.to_csv('courses.csv')
print(df)


