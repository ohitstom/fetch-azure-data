import os
import sys
import webbrowser
import pyperclip

from modules.globals import app, scopes
from modules import layout, updateActivity, updateAll, updateEmails

def main(result, token):
    selectionDict ={
        1: updateAll.run,
        2: updateActivity.run,
        3: updateEmails.run,
        4: sys.exit
    }    
    selection = input(layout.selection % (f"{result['id_token_claims']['name']}\nYour login will expire in: {round(int(result['expires_in']) / 60)} minutes"))
    if selection.isdigit() and int(selection) in selectionDict:
        os.system('cls')
        print(selectionDict[int(selection)](token if int(selection) != 4 else None))

    else:
        os.system('cls')
        print("Invalid Selection")
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
