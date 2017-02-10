#!/bin/bash
if [ $# -ne 2 ]
  then
    echo "Usage: ./find_existing_joka_installs.sh <pulse_install_dir> <pulse_common_dir>"
    exit 0;
fi

PULSE_INSTALL_DIR=${1}
PULSE_COMMON_DIR=${2}

for ii in $(find ${PULSE_INSTALL_DIR} -maxdepth 1 -type d -name "joka-*" -print)
do
  echo $ii
  if [ $(find ${ii} -type d -name "app" | wc -l) != "0" ]
  then
    configs=$(find "${ii}/app" -type d -name "configs" -print -quit)
    echo ${configs}
    cp -rf ${configs} ${PULSE_COMMON_DIR}
    break
  fi
done
