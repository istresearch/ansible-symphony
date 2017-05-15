#!/bin/bash
if [ $# -ne 3 ]
  then
    echo "Usage: ./copy_pulse_files.sh <joka_version> <pulse_ui_version> <pollster_version>"
    exit 0;
fi

JOKA_VERSION=${1}
PULSE_UI_VERSION=${2}
POLLSTER_VERSION=${3}

if [ -f "joka-${JOKA_VERSION}.zip" ]
then
  cp -f joka-${JOKA_VERSION}.zip /tmp/joka-${JOKA_VERSION}.zip
fi

if [ -f "pulse-ui-${PULSE_UI_VERSION}.tar.gz" ]
then
  cp -f pulse-ui-${PULSE_UI_VERSION}.tar.gz /tmp/pulse-ui-${PULSE_UI_VERSION}.tar.gz
fi

if [ -f "appPollsterPrime-post23-release-${POLLSTER_VERSION}.apk" ]
then
  cp -f appPollsterPrime-post23-release-${POLLSTER_VERSION}.apk /tmp/appPollsterPrime-post23-release-${POLLSTER_VERSION}.apk  
fi

if [ -f "appPollsterPrime-pre23-release-${POLLSTER_VERSION}.apk" ]
then
  cp -f appPollsterPrime-pre23-release-${POLLSTER_VERSION}.apk /tmp/appPollsterPrime-pre23-release-${POLLSTER_VERSION}.apk  
fi

if [ -f "backup.tar" ]
then 
  cp -f backup.tar /tmp/backup.tar
fi

if [ -f "joka_nuke.zip" ]
then 
  cp -f joka_nuke.zip /tmp/joka_nuke.zip
fi
