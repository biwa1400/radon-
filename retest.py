import re
 
pattern = re.compile(r'.*(devicePATH=)(.*)(;).*')
 
match = pattern.match('<?xml version="1.0" encoding="UTF-8"?><api version="1.0"><header><function>switchMode</function>devicePATH=/dev/ttyUSB0;')
 
if match:

    print (match.group(2))
 
