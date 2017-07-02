## Hass.io plugins

[![Build Status](https://travis-ci.org/vkorn/hassio-addons.svg?branch=master)](https://travis-ci.org/vkorn/hassio-addons)

## Pre-built images

## [SmartThings](https://github.com/vkorn/hassio-addons/tree/master/smartthings) [![](https://images.microbadger.com/badges/version/vkorn/armhf-smartthings.svg)](https://microbadger.com/images/vkorn/armhf-smartthings "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/vkorn/armhf-smartthings.svg)](https://microbadger.com/images/vkorn/armhf-smartthings "Get your own image badge on microbadger.com")

SmartThings MQQT Bridge

## [PS4Waker](https://github.com/vkorn/hassio-addons/tree/master/ps4waker) [![](https://images.microbadger.com/badges/version/vkorn/armhf-ps4waker.svg)](https://microbadger.com/images/vkorn/armhf-ps4waker "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/vkorn/armhf-ps4waker.svg)](https://microbadger.com/images/vkorn/armhf-ps4waker "Get your own image badge on microbadger.com")

REST-wrapper arodun ps4-waker to support ps4 component

## [DeviceLocator](https://github.com/vkorn/hassio-addons/tree/master/devicelocator) [![](https://images.microbadger.com/badges/version/vkorn/armhf-devicelocator.svg)](https://microbadger.com/images/vkorn/armhf-devicelocator "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/vkorn/armhf-devicelocator.svg)](https://microbadger.com/images/vkorn/armhf-devicelocator "Get your own image badge on microbadger.com")

Simple service which will return IP of callind device. Useful for UI tweaking only.


## [ConfigWatcher](https://github.com/vkorn/hassio-addons/tree/master/configwatcher) [![](https://images.microbadger.com/badges/version/vkorn/armhf-configwatcher.svg)](https://microbadger.com/images/vkorn/armhf-configwatcher "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/vkorn/armhf-configwatcher.svg)](https://microbadger.com/images/vkorn/armhf-configwatcher "Get your own image badge on microbadger.com")

Config watchdog which will perform restarts if required. 

## Just code

These add-ons are not being built intentionally as they are for testing purposes only. You'll need to download and place them under `/addons` folder of your Hass.io instance. 

## [AppDaemon](https://github.com/vkorn/hassio-addons/tree/master/appdaemon)

Beta-version of AppDaemon with HaDashobard v2.

## Usefull commands

If you're getting too much stalled containers, run (warning, can damage you setup!!!)

```
docker rm -v $(docker ps --filter status=exited -q 2>/dev/null)
docker rm -v $(docker ps --filter status=created -q 2>/dev/null)
```
Similar can be done for images.