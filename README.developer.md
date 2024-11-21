# Arduino logger

## Χρήση

cd alx_arduino_logger

### Linux



### Windows




## How to build 

### Linux

01. Create the python virtual environment

virtualenv linuxenv

source linuxenv/bin/activate

02. Install Linux requirements

pip install -r requirements.txt

03. Package app

pyinstaller alx_arduino_monitor.spec


### Windows

01. Create the python virtual environment

py -m venv env

env\Scripts\activate

02. Install Windows requirements

py -m pip install -r requirements_windows.txt

03. Package app

C:\Users\<USERNAME>\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe alx_arduino_monitor_windows.spec

https://earthly.dev/blog/pyinstaller/#:~:text=Using%20a%20Python%20Virtual%20Environment%20with%20PyInstaller%201,and%20Executable%20...%204%20Testing%20the%20Executable%20

pyinstaller quick start

https://pyinstaller.org/en/stable/
https://stackoverflow.com/questions/48757977/how-to-include-dependencies-from-venv-directory-when-running-pyinstaller-for-pro
https://stackoverflow.com/questions/63585632/how-to-add-a-truetype-font-file-to-a-pyinstaller-executable-for-use-with-pygame


