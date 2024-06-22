# usbdriver-fix

Fix cause and symptoms of USBDriver.exe virus on the host and USB drives.

There's an annoying virus that hides files on USB drives and only shows a file
called "USBDriver.exe". If a user double-clicks this file, then "MSBuild.exe" is
installed into C:\Users\Public\Library and is started as a Windows service. This
executable will then corrupt any USB drive plugged into the system by hiding its
files as mentioned above.

This app is intended to fix this problem in two ways:
1. Recover the hidden files on a USB drive and remove USBDriver.exe from it.
1. Stop the MSBuild.exe service in the host computer and delete the MSBuild.exe
   file from the host to prevent further infections.
