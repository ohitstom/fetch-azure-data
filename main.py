import os
import sys
import webbrowser
import pyperclip
import asyncio
import json
import datetime

from modules import layout, updateActivity, updateAll, updateEmails, utils

async def main(package):
    selectionDict ={
        1: updateAll.run,
        2: updateActivity.run,
        3: updateEmails.run,
        4: sys.exit
    }    
    
    selection = input(layout.selection % (f"{package['User']}\nYour login will expire at: {package['Expiry']}"))
    if selection.isdigit() and int(selection) in selectionDict:
        os.system('cls')
        print(await (selectionDict[int(selection)](package['Token'] if int(selection) != 4 else None)))
    else:
        os.system('cls')
        print("Invalid Selection")
        await main(package)

    menuReturn = input("\nReturn? (Y/N) -> ").lower()
    if menuReturn == "y":
        os.system('cls')
        await main(package)
    else:
        await utils.shutdown()

async def login():
    # Microsoft login and creation of data
    await utils.powershell('Clear-AzContext -Force', wait=True, verbose=False)
    await utils.powershell('Connect-AzAccount', wait=True, verbose=False)
    await utils.powershell('Connect-MgGraph -Scopes "User.Read", "User.Read.All", "Directory.Read.All", "Group.Read.All"', wait=True, verbose=False)
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
    os.system('cls')
    await main(package)

async def package_check():
    print("Checking for AzureAD powershell module")
    azuread_proc = await utils.powershell("Get-Module -ListAvailable -Name AzureAD", wait=True, verbose=False)
    azuread = (await azuread_proc.stdout.read()).decode("utf-8")
    
    azread_proc = await utils.powershell("Get-Module -ListAvailable -Name Az.Accounts", wait=True, verbose=False)
    azread = (await azread_proc.stdout.read()).decode("utf-8")

    if azuread != "" and azread != "":
        print("AzureAD and Az.Accounts powershell modules installed")
        await login()

    if azuread == "":
        print("AzureAD powershell module not installed")
        print("Installing AzureAD powershell module")
        await utils.powershell("Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force", wait=True, verbose=False)
        install_proc = await utils.powershell("Install-Module -Name AzureAD -Scope CurrentUser -Force", wait=True, verbose=False)
        install = (await install_proc.stdout.read()).decode("utf-8")
        if install == "":
            print("AzureAD powershell module installed")
        else:
            print("Error installing AzureAD powershell module")
            print("Please install AzureAD powershell module manually")
            print("Exiting...")
            sys.exit()
    
    if azread == "":
        print("Az.Accounts powershell module not installed")
        print("Installing Az.Accounts powershell module (This can take a long time)")
        install_proc = await utils.powershell("Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force", wait=True, verbose=False)
        install = (await install_proc.read()).decode("utf-8")
        if install == "":
            print("Az.Accounts powershell module installed")
        else:
            print("Error installing Az.Accounts powershell module")
            print("Please install Az.Accounts powershell module manually")
            print("Exiting...")
            sys.exit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(package_check())