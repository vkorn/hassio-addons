## HASS AppDaemon Add-on for Hass.io

This addon uses beta-branch of AppDaemon with HaDashboard v2. Please refer to [official repo](https://github.com/home-assistant/appdaemon/tree/hadashboard_beta) for configuration details.

You can configure following 2 options through UI (main config located at `/config/hadaemon` folder):

| Param          | Description              |
|----------------|--------------------------|
| commtype		 | Communication protocol for HASS, only SSE works now      |
| domain		 | Domain you're going to use for dashboard (details below) |


Please note, right now it's not possible to have different binding and rendering URLs for Dashboard. To handle this, port 80 is used by default (exposed as `3030` from docker). 
You'll need to use nginx proxy, for example this [addon](https://github.com/bestlibre/hassio-addons/tree/master/nginx_proxy) works really well.