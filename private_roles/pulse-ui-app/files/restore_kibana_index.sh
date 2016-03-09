#!/bin/bash
if [ $# -ne 3 ]
  then
    echo "Usage: ./restore_kibana_index.sh <es_location> <es_port> <backup_tar>"
    exit 0;
fi

# unpack tar
tar xvf ${3}
FOLDER=${3%.*}
cd $FOLDER

# for each index in folder
for index in $(ls -a)
do
  # ignore linux . .. and mac .DS_STORE
  if [ "$index" != "." ] && [ "$index" != ".." ] && [ "$index" != ".DS_Store" ]
  then
    cd $index
    /usr/bin/curl -XPUT ${1}:${2}/$index -T "$index"
    # for each type
    for type in $(ls -a -d -- */)
    do
      # ignore linux . .. and mac .DS_STORE
      if [ "$type" != "." ] && [ "$type" != ".." ] && [ "$type" != ".DS_Store" ]
      then
        cd $type
        # for each item
        for item in $(ls -a)
        do
          # ignore linux . .. and mac .DS_STORE
          if [ "$item" != "." ] && [ "$item" != ".." ] && [ "$item" != ".DS_Store" ]
          then
            #echo "/usr/bin/curl -XPUT ${1}:${2}/$index/$type/$item -T $item"
            /usr/bin/curl -XPUT ${1}:${2}/$index/$type/$item -T $item
          fi
        done
        cd ../
      fi
    done
    cd ../
  fi
done
cd ../
# clean up unpacked folder
rm -rf $FOLDER
