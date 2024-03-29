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
        print("Clearing Login...")
        await utils.powershell('Clear-AzContext -Force', wait=True)
        os.system('cls')
        os._exit(0)

async def login():
    # Clearing Previous Logins
    print("\nSanitizing Azure Context...")
    await utils.powershell('Clear-AzContext -Force', wait=True)
    
    # Microsoft login and creation of data
    print("Preparing for login...")
    process = await utils.powershell(
        '\n'.join([
            '$DebugPreference = "Continue"' if globals.verbose else '$DebugPreference = "SilentlyContinue"',
            'Connect-AzAccount -UseDeviceAuthentication'
        ]),
        wait=True,
        account_proc=True
    )

    print("Waiting for login success...")
    access_proc = await utils.powershell("Get-AzAccessToken -ResourceUrl 'https://graph.microsoft.com/' | ConvertTo-Json", wait=True, verbose=False)
    access = (await access_proc.stdout.read()).decode("utf-8")
    
    if "Token" not in access:
        print("Connection Failed, verbose has been printed to console.")
        print(access)
        input("Press any key to exit...")
        os._exit(0)
        
    json = json.loads(access)
    package = {
        'Token': json['Token'],
        'Expiry': int(''.join(filter(str.isdigit, json['ExpiresOn']))),
        'User': json['UserId']
    }

    # Epoch to datetime
    package['Expiry'] = datetime.datetime.fromtimestamp(package['Expiry'] / 1e3).strftime('%Y-%m-%d %H:%M:%S')

    # Main Function
    os.system('cls')
    await main(package)

async def package_check():
    # Checking Packages
    print("Checking for powershell modules...")
    process = await utils.powershell("@((Get-Module 'AzureAD', 'Az.Accounts' -ListAvailable).Name | Select-Object -Unique)", wait=True, verbose=False)
    check_out = '\n'.join((await process.stdout.read()).decode("utf-8").strip().splitlines()[-2:])

    if globals.verbose:
        print(check_out)

    if {'AzureAD', 'Az.Accounts'}.issubset(check_out):
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
