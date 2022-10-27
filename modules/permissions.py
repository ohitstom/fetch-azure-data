from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient 
from modules.globals import *
from modules import utils

def run():
    try:
        credentials=ClientSecretCredential(tenant_id=tenantid,client_id=clientid,client_secret=clientsecret) 
        graph_client = GraphClient(credential=credentials)
        users = graph_client.get('/users').json()
        utils.exportJson(utils.prettier(users), "user_list.json")
        return "Completed"
    except Exception as e:
        return e

