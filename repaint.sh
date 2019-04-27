#!/bin/bash
echo "------Repaint My Wall------"
echo "--Author: Jayesh Kulkarni--"


if [ -z "$1" ]
then
	echo "No wallpaper tag specified! Getting a wallpaper for tag 'Sea'"
	tag="sea"
else
	tag=$1
fi

tempDir=/home/$( whoami )/repaint
cnt=$(find $tempDir 2> /dev/null | wc -l)

if [ $cnt -eq 0 ] 
then
	mkdir $tempDir
fi

function getNextWallpaper {
	echo "Initiating API call..."
	link=$(	curl "https://api.unsplash.com/photos/random?client_id=cbe31d9f91f95d0d35be45aca596919deff0cf47ee01a684ff8323aec482278f&query=$tag" | jq -r '.urls.full' )

	if [ $link != "" ]
	then
		wget -O  ${tempDir}/newWall.jpg $link > /dev/null
		echo "API call completed successfully!"
		gsettings set org.gnome.desktop.background picture-uri  'file:'${tempDir}'/newWall.jpg'
		cp ${tempDir}/newWall.jpg /var/lib/lightdm-data/$( whoami )/wallpaper/
		notify-send 'New wallpaper applied successfully' -i stock_smiley-15
	else
		echo "Error while attempting API call!"
	fi

}

getNextWallpaper

