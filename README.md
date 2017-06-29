## Hass.io plugins

Please note that images are not pre-built for now. You'll need to download and place them under /addons folder of your Hass.io instance. 

If you're getting too much stalled images, run (warning, can damage you setup!!!)

```
docker rm -v $(docker ps --filter status=exited -q 2>/dev/null)
```

Or created but not running

```
docker rm -v $(docker ps --filter status=created -q 2>/dev/null)
```