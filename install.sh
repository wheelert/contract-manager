#!/bin/bash

# zenity
if ! command -v zenity &> /dev/null; then
    echo -e "\e[33m you must install zenity (pacman -S zenity or apt install zenity) \e[0m"
	exit
fi



if zenity --question --text="Install Contract Manager?"; then

APPDIR=~/.local/share/contract-manager

(
	echo "10"
	echo "#Checking for previous versions"
	sleep 2
	if [ -d "$APPDIR" ]; then
	echo "20"
	echo "#removing older version files"
	    rm -rf $APPDIR
	    rm ~/.local/share/applications/contract-manager.desktop
	fi
	  sleep 2
	 echo "50"
	 echo "#Installing Contract Manager"
	mkdir $APPDIR
	cp src/*.py $APPDIR

	cp src/contract_manager.png $APPDIR
	cp src/contract-manager.desktop ~/.local/share/applications/
	  sleep 2
	 echo "100"
	 echo "# Done!"
) | zenity --progress \
  --title="Installing Contract Manager" \
  --text="installing..." \
  --percentage=0 \
  --auto-close
  
 

else
    exit 1
fi