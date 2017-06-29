## Returning IP and device info if known

In some cases it's useful to understand on UI which device is performing requests. 
This tiny service can take same `hosts` as 
[DHCP plugin](https://home-assistant.io/addons/dhcp_server/) and will return device name 
if known in addition to IP. 
