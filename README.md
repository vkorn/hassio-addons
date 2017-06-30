## Hass.io plugins

[![Build Status](https://travis-ci.org/vkorn/hassio-addons.svg?branch=master)](https://travis-ci.org/vkorn/hassio-addons)

Following addons are built: 

## [SmartThings](https://github.com/vkorn/hassio-addons/tree/master/smartthings) [![](https://images.microbadger.com/badges/version/vkorn/armhf-smartthings.svg)](https://microbadger.com/images/vkorn/armhf-smartthings "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/vkorn/armhf-smartthings.svg)](https://microbadger.com/images/vkorn/armhf-smartthings "Get your own image badge on microbadger.com")

SmartThings MQQT Bridge



Other addons are not being built intentionally as they are for testing purposes only. You'll need to download and place them under `/addons` folder of your Hass.io instance. 

If you're getting too much stalled images, run (warning, can damage you setup!!!)

```
docker rm -v $(docker ps --filter status=exited -q 2>/dev/null)
```

Or created but not running

```
docker rm -v $(docker ps --filter status=created -q 2>/dev/null)
```