#!/bin/bash
xmlFilePath="/home/biwa1400/share/radon++/scripts/sw_debug_mode.xml"
usb_modeswitch -v 12d1 -p 1f01 -c /usr/share/usb_modeswitch/12d1\:1f01
sleep 2
#ifconfig eth1 up
#udhcpc -BFs -i eth1
curl -X POST -m 1 -d @$xmlFilePath http://192.168.8.1/CGI 


sleep 3

deviceInfo="HUAWEI_MOBILE
1566
12d1"

i=0;

for device in $(ls /dev/ttyUSB*)
do
        a=$(udevadm info $device | grep 'ID_MODEL_ENC\|ID_MODEL_ID\|ID_VENDOR_ID' |sed 's/.*=//g');
        if [ "$a" = "$deviceInfo" ];then
                echo 'devicePATH='$device';'
                break
        fi
done

