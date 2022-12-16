nuitka --onefile --include-plugin-directory=modules --enable-plugin=numpy main.py
Start-Sleep -Seconds 1.5
Remove-Item -LiteralPath "main.build" -Force -Recurse
Remove-Item -LiteralPath "main.dist" -Force -Recurse
Remove-Item -LiteralPath "main.onefile-build" -Force -Recurse
New-Item "build" -itemType Directory
Move-Item -Path main.exe -Destination build\main.exe