# Arduino logger

## Χρήση

cd alx_arduino_logger

### Linux



### Windows




## How to build 

### Linux

00. Create the python virtual environment && activate it
 
virtualenv linuxenv

source linuxenv/bin/activate

01. Install Linux requirements

(linuxenv) pip install -r requirements.txt

02. Package app

(linuxenv) pyinstaller alx_arduino_monitor.spec


### Windows

00. Create the python virtual environment && activate it

py -m venv env

env\Scripts\activate

01. Install Windows requirements

(env) py -m pip install -r requirements_windows.txt

02. Package app

(env) py -m PyInstaller alx_arduino_monitor_windows.spec

https://earthly.dev/blog/pyinstaller/#:~:text=Using%20a%20Python%20Virtual%20Environment%20with%20PyInstaller%201,and%20Executable%20...%204%20Testing%20the%20Executable%20

pyinstaller quick start

https://pyinstaller.org/en/stable/
https://stackoverflow.com/questions/48757977/how-to-include-dependencies-from-venv-directory-when-running-pyinstaller-for-pro
https://stackoverflow.com/questions/63585632/how-to-add-a-truetype-font-file-to-a-pyinstaller-executable-for-use-with-pygame


