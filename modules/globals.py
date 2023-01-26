verbose = None

base_url = "https://graph.microsoft.com/"

arg_dict = {
    "verbose": {
        "commands": ["--verbose", "-v"],
        "description": "Logs Extra Information For Debugging Purposes",
        "action": "globals.verbose = True",
        "continue": True
    },

    "help": {
        "commands": ["--help", "-h"],
        "description": "Displays Help Menu",
        "action": "print(arg_help)",
        "continue": False
    }
}

arg_help = "Help Menu:\n" + "".join(
    f"{value['commands'][0]} ({value['commands'][1]}): {arg_dict[arg]['description']}\n"
    for arg, value in arg_dict.items()
)