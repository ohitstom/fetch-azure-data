import webbrowser
import requests
import msal
from msal import PublicClientApplication

#https://www.youtube.com/watch?v=1Jyd7SA-0kI&list=WL&index=74

APPLICATION_ID = "4c8d41bc-0a4d-4985-aa15-8c7be46eb52a"
CLIENT_SECRET = "Oz68Q~69rMXGV2PWhbGQkO_bP2.YZ5HIKxd.ecJA"
authority_url = "https://login.microsoftonline.com/ffb75476-0afa-47b0-9b8c-6f97809370fe"
base_url = "https://graph.microsoft.com/v1.0"
scopes = ["User.Read"]

app = PublicClientApplication(
    APPLICATION_ID, 
    authority=authority_url
    )

flow = app.initiate_device_flow(scopes=scopes)
print(flow["message"])
webbrowser.open(flow["verification_uri"])

result = app.acquire_token_by_device_flow(flow)
print(result)
access_token = result["access_token"]
headers = {"Authorization": "Bearer " + access_token}

endpoint = base_url + "/me"
response = requests.get(endpoint, headers=headers)
print(response.json())