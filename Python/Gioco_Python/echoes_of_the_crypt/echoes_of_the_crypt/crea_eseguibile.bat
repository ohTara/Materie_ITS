@echo off
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m PyInstaller --noconfirm --clean EchoesOfTheCrypt.spec
powershell Compress-Archive -Path dist\EchoesOfTheCrypt -DestinationPath EchoesOfTheCrypt.zip -Force
echo Fatto: EchoesOfTheCrypt.zip pronto da condividere
pause