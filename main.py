import sys
import os
from modules import layout, updateUser, updateAll

def main():
    selectionDict ={
        1: updateAll.run,
        2: updateUser.run,
        3: sys.exit
    }    
    selection = input(layout.selection)
    if selection.isdigit() and int(selection) in selectionDict:
        print(selectionDict[int(selection)]())    
    else:
        os.system('cls')
        print("Invalid Selection")
        main()
    
    menuReturn = input("Return? (Y/N) -> ").lower()
    if menuReturn == "y":
        os.system('cls')
        main()
    else:
        sys.exit

if __name__ == "__main__":
    main()