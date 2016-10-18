#!/bin/bash
if [ $# -ne 4 ]
  then
    echo "Usage: ./backup_kibana_index.sh <es_location> <es_port> <backup_folder> <index_name>"
    exit 0;
fi

pullIndex () {
  # make index dir backup
  mkdir -p ${3}
  cd ${3}
  # store index config
  curl -s -X GET ${1}:${2}/${3} > ${3}

  # if you have more than 100000 items in your kibana4 setup then we have other issues...
  # grab all elasticsearch results for particular type
  OUTPUT=$(curl -s -X GET ${1}:${2}/${3}/_search?size=10000)

  # grab hits for search query
  OUTPUT=$(echo $OUTPUT | grep -o '\[.*\]')

  # trim leading and end of source files
  OUTPUT=${OUTPUT%?}
  OUTPUT=${OUTPUT#*:}
  #echo $OUTPUT

  # split into storable json pieces, store to temp file split on new lines
  echo $OUTPUT | awk 'BEGIN {FS=",{\"_index\""} {for(i=1;i<=NF;i++){ print $i > "temp.txt" }}'
  # save old field separator
  OLD_IFS=$IFS
  IFS=$'\n'
  # parse temp file
  for line in $(cat temp.txt)
  do
     # grab important pieces
     TYPE=$(echo $line | cut -d '"' -f 6)
     ID=$(echo $line | cut -d '"' -f 10)
     SOURCE=${line#*\"_source\":}
     SOURCE=${SOURCE%?} # trime last }

     # store file
     mkdir -p $TYPE
     echo $SOURCE > $TYPE/$ID
  done
  IFS=$OLD_IFS     # restore default field separator
  rm -f "temp.txt"
  cd ../
}

mkdir -p ${3}
cd ${3}
pullIndex ${1} ${2} ${4}
cd ../

# pack folder
tar cvf ${3}.tar ${3}
# clean up
rm -rf ${3}
