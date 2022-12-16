<<<<<<< HEAD
import msal
from msal import PublicClientApplication

APPLICATION_ID = "4c8d41bc-0a4d-4985-aa15-8c7be46eb52a"
authority_url = "https://login.microsoftonline.com/ffb75476-0afa-47b0-9b8c-6f97809370fe"
base_url = "https://graph.microsoft.com/"
scopes = ["User.Read", "User.Read.All", "Directory.Read.All", "Group.Read.All"]
app = PublicClientApplication(APPLICATION_ID, authority=authority_url)
=======
base_url = "https://graph.microsoft.com/"
>>>>>>> 5e80d19 (2:32)
