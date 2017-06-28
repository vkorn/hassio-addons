## HASS AppDaemon Add-on for Hass.io

This is beta-branch which allows you to use HaDashboard v2. Please refer to [official repo](https://github.com/home-assistant/appdaemon/tree/hadashboard_beta) for configuration details.

In Hass.io there're 2 available options: 

| Param          | Description              |
|----------------|--------------------------|
| commtype		 | Communication protocol for HASS, only SSE works now      |
| domain		 | Domain you're going to use for dashboard (details below) |


Please note, right now it's not possible to have different binding and rendering URLs for Dashboard, port 80 is used by default internally and 3030 exposed from Docker. You'll need to use nginx proxy to fix this, for example this [plugin](https://github.com/bestlibre/hassio-addons/tree/master/nginx_proxy).