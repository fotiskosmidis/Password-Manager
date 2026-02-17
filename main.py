import bindings # type: ignore // This is for ignoring the warning from Pylance in VSCode
import os

import frontEnd.loginWindow as loginWindow
import frontEnd.createPasswdWindow as createPasswdWindow

# Check if the user has already set a pin, if not, open the create pin window, otherwise open the login window
if os.path.exists("DBfiles/settings.json"):
        loginWindow.loginWindow()
else:
        passwd = createPasswdWindow.createPasswdWindow()
        if passwd != "":
                bindings.createKey(passwd)
                loginWindow.loginWindow()
        else:
                # error happened while creating the pin, close the program
                exit()



