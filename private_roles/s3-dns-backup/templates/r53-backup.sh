#!/bin/bash
today=`date  +"%m-%d-%Y"`
mkdir $today
/usr/local/bin/aws route53 list-hosted-zones | /usr/bin/jq -r  '.HostedZones[] | .Id +" "+ .Name + " " + [.Config.PrivateZone | tostring][0]' |
while read zoneentry 
do
read -a zoneinfo <<< "$zoneentry"
zoneid="${zoneinfo[0]}"
justzoneid=`echo $zoneid | awk -F "/" '{print  $3}' `
zonename="${zoneinfo[1]}"
zoneprivate="${zoneinfo[2]}"
case "$zoneprivate" in
	"false") zonestatus="public";;
	"true") zonestatus="private";;
esac

zonefilename="$justzoneid-$zonename$zonestatus"
jsonfilename="$zonefilename.json"
textfilename="$zonefilename.txt"
/usr/local/bin/aws route53 list-resource-record-sets --hosted-zone-id  $justzoneid > $today/$jsonfilename
/usr/local/bin/aws route53 list-resource-record-sets --output text --hosted-zone-id  $justzoneid > $today/$textfilename
/usr/local/bin/aws s3 cp $today/$jsonfilename s3://dns-backup-ist/$today/
/usr/local/bin/aws s3 cp $today/$textfilename s3://dns-backup-ist/$today/
done
rm -rf $today

