Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
Install-Module -Name AzureAD -Scope CurrentUser -Force
Install-Module -Name Az.Accounts -Scope CurrentUser -Repository PSGallery -Force