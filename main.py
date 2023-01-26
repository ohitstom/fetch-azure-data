import os
import sys
import asyncio
import json
import datetime

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
        logger._pause_file_output = False
    else:
        os.system('cls')
        print("Invalid Selection")
        await main(package)

    menuReturn = input("\nReturn? (Y/N) -> ").lower()
    if menuReturn == "y":
        os.system('cls')
        await main(package)
    else:
        print("Clearing Login And Disconnecting From Graph...")
        await utils.powershell('Disconnect-MgGraph', wait=True)
        await utils.powershell('Clear-AzContext -Force', wait=True)
        os.system('cls')
        os._exit(0)

async def login():
    # Clearing Previous Logins
    print("\nSanitizing Azure Context...")
    await utils.powershell("Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force", wait=True)
    await utils.powershell('Clear-AzContext -Force', wait=True)
    
    # Microsoft login and creation of data
    print("Prompting for login...")
    await utils.powershell('Connect-AzAccount', wait=True)
    print("Connecting to Microsoft Graph...")
    await utils.powershell('Connect-MgGraph -Scopes "User.Read", "User.Read.All", "Directory.Read.All", "Group.Read.All"', wait=True)
    access_proc = await utils.powershell("Get-AzAccessToken -ResourceUrl 'https://graph.microsoft.com/' | ConvertTo-Json", wait=True, verbose=False)
    access = (await access_proc.stdout.read()).decode("utf-8")
    
    if "Token" not in access:
        print("Connection Failed, verbose has been printed to console.")
        print(access)
        input("Press any key to exit...")
        os._exit(0)
        
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
    # Checking Packages
    print("Checking for powershell modules...")
    azuread_proc = await utils.powershell("Get-Module -ListAvailable -Name AzureAD", wait=True)
    azread_proc = await utils.powershell("Get-Module -ListAvailable -Name Az.Accounts", wait=True)
    
    azuread = (await azuread_proc.stdout.read()).decode("utf-8")
    azread = (await azread_proc.stdout.read()).decode("utf-8")

    if azuread == "" or azread == "":
        print("AzureAD or Az.Accounts powershell module not installed\n Please run dependencies.ps1 as admin.")
        input("Press any key to exit...")
        os._exit(0)
    else:
        print("Powershell modules installed")
        await login()

if __name__ == "__main__":
    from modules import logger
    from modules import layout, updateActivity, updateAll, updateEmails, utils, globals

    args = "\n".join(sys.argv[1:])
    if len(args) <= 1:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(package_check())
    else:
        for item in globals.arg_dict:
            if args in globals.arg_dict[item]['commands']:
                exec(globals.arg_dict[item]['action'])
                if globals.arg_dict[item]['continue']:
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(package_check())
                break
        else:
            print(f"Invalid Argument: {args}\n")
            print(globals.arg_help)
