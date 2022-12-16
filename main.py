import os
import sys
import webbrowser
import pyperclip
<<<<<<< HEAD

from modules.globals import app, scopes
from modules import layout, updateActivity, updateAll, updateEmails

def main(result, token):
=======
import asyncio
import json
import datetime

from modules import layout, updateActivity, updateAll, updateEmails, utils

async def main(package):
>>>>>>> 5e80d19 (2:32)
    selectionDict ={
        1: updateAll.run,
        2: updateActivity.run,
        3: updateEmails.run,
        4: sys.exit
    }    
<<<<<<< HEAD
    selection = input(layout.selection % (f"{result['id_token_claims']['name']}\nYour login will expire in: {round(int(result['expires_in']) / 60)} minutes"))
    if selection.isdigit() and int(selection) in selectionDict:
        os.system('cls')
        print(selectionDict[int(selection)](token if int(selection) != 4 else None))
=======
    selection = input(layout.selection % (f"{package['User']}\nYour login will expire at: {package['Expiry']}"))
    if selection.isdigit() and int(selection) in selectionDict:
        os.system('cls')
        print(await (selectionDict[int(selection)](package['Token'] if int(selection) != 4 else None)))
>>>>>>> 5e80d19 (2:32)

    else:
        os.system('cls')
        print("Invalid Selection")
<<<<<<< HEAD
        main(result, token)
    menuReturn = input("\nReturn? (Y/N) -> ").lower()
    if menuReturn == "y":
        os.system('cls')
        main(result, token)
    else:
        sys.exit

def login():
    # Prompt user to sign in
    flow = app.initiate_device_flow(scopes=scopes)
    print(f"{flow['message']}\n\nThis code has been copied to your clipboard and expires in: {round(int(flow['expires_in']) / 60)} minutes.")
    pyperclip.copy(flow["user_code"])
    webbrowser.open(flow["verification_uri"])

    # Acquire JWT from login
    result = app.acquire_token_by_device_flow(flow)

    if result["access_token"]:
        os.system('cls')
        main(result, result["access_token"])
    else:
        os.system('cls')
        print("Failed to acquire token: ", print(result['error'], result['error_description']))
        login()


if __name__ == "__main__":
    login()
=======
        await main(package)
    menuReturn = input("\nReturn? (Y/N) -> ").lower()
    if menuReturn == "y":
        os.system('cls')
        await main(package)
    else:
        sys.exit

async def login():
    # Microsoft login and creation of data
    connect = await utils.powershell('Connect-MgGraph -Scopes "User.Read", "User.Read.All", "Directory.Read.All", "Group.Read.All" | Out-Null', wait=True, verbose=False)
    access_proc = await utils.powershell("Get-AzAccessToken -ResourceUrl 'https://graph.microsoft.com/' | ConvertTo-Json", wait=True, verbose=False)
    access = (await access_proc.stdout.read()).decode("utf-8")
    package = {
        'Token': json.loads(access)['Token'],
        'Expiry': int(''.join(filter(str.isdigit, json.loads(access)['ExpiresOn']))),
        'User': json.loads(access)['UserId']
    }

    # Epoch to datetime
    package['Expiry'] = datetime.datetime.fromtimestamp(package['Expiry'] / 1e3).strftime('%Y-%m-%d %H:%M:%S')
    
    # Main Function
    await main(package)

async def package_check():
    print("Checking for AzureAD powershell module")
    azuread_proc = await utils.powershell("Get-Module -ListAvailable -Name AzureAD", wait=True, verbose=False)
    azuread = (await azuread_proc.stdout.read()).decode("utf-8")
    
    if azuread == "[]":
        print("AzureAD powershell module not installed")
        print("Installing AzureAD powershell module")
        install_proc = await utils.powershell("Install-Module -Name AzureAD -Scope CurrentUser -Force", wait=True, verbose=False)
        install = (await install_proc.stdout.read()).decode("utf-8")
        if install == "":
            print("AzureAD powershell module installed")
            await login()
        else:
            print("Error installing AzureAD powershell module")
            print("Please install AzureAD powershell module manually")
            print("Exiting...")
            sys.exit()
    else:
        print("AzureAD powershell module found")
        await login()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(package_check())
>>>>>>> 5e80d19 (2:32)
