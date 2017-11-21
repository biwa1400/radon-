#1. find usb device
#ls /dev/ttyUSB* | cat -A
deviceInfo="HUAWEI_MOBILE
1566
12d1"

i=0;

for device in $(ls /dev/ttyUSB*)
do
	a=$(udevadm info $device | grep 'ID_MODEL_ENC\|ID_MODEL_ID\|ID_VENDOR_ID' |sed 's/.*=//g');
	if [ "$a" = "$deviceInfo" ];then
		echo 'device='$device
		break
	fi
done




#a= udevadm info /dev/ttyUSB1
#echo 'dabin'
#echo $a

