## PS4-Waker REST service

Original [PS4 component](https://community.home-assistant.io/t/playstation-4-ps4-custom-component/16974) requires nodejs package to work. This small addon will run REST-wrapper around [ps4-waker](https://github.com/dhleong/ps4-waker) and serve it's data to slighly changed PS4 component (`hass/custom_components` folder).

Component now has a bit different configuration: 

```
host -- now this is address where add-on is listening, e.g. host: http://10.0.0.1:3031
ps4_ip -- IP of device

```

Credentials for ps4-waker should be configured through Hassio UI.

> Please refer to [this](https://community.home-assistant.io/t/playstation-4-ps4-custom-component/16974/73) post for details of how to install and use this addon 
