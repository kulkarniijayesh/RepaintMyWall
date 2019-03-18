#!/bin/bash
echo "------Repaint My Wall------"
echo "--Author: Jayesh Kulkarni--"
tempDir=/tmp/repaint
cnt=$(find $tempDir 2> /dev/null | wc -l)
if [ $cnt -eq 0 ] 
then
	mkdir /tmp/repaint
fi

function getNextWallpaper {
	echo "Initiating API call..."
	link=$(	curl "https://api.unsplash.com/photos/random?client_id=cbe31d9f91f95d0d35be45aca596919deff0cf47ee01a684ff8323aec482278f&collections=1922729" | jq -r '.urls.full' )

	if [ $link != "" ]
	then
		wget -O  ${tempDir}/newWall.jpg $link > /dev/null
		echo "API call completed successfully!"
		gsettings set org.gnome.desktop.background picture-uri  'file:/tmp/repaint/newWall.jpg'
	else
		echo "Error while attempting API call!"
	fi

}

getNextWallpaper

