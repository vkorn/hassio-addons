## Hass.io plugins

Please note that images are not pre-built for now. You'll need to donload and plase them under /addons dir on your Hass.io instance. 

If you're getting too much stalled images, run (warning, can damager you setup!!!)

```
docker rm -v $(docker ps --filter status=exited -q 2>/dev/null)
```