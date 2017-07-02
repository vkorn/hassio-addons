## Config sync

This add-on will use local git to update your configuration and restart addons and 
HASS itself if there were any changes. 

>This addon might not work for you if you have plain structure or keep everything inside 
`/config` folder without sub-directories, as it will require too much configuration. 

### Prerequisites
1. Clone your repository manually (using ssh or sshfs)
2. Create ouath token (you can skip this step and user you real password but it's strongly not advised): 
    - for bitbucket it's [app password](https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html)
    - for github it's [personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)
3. Modify .git/config file and include your password (e.g. https://user:token@github...)


### Configuration

| Param | Description|
|:----------------------|:---------------------|
| base_dir      | Absolute path to your config folder, defaults to `/config` |
| check_delay   | Interval in **minutes** between git pulls, defaults to `1` |
| hassio_host   | Hass.io API including scheme, defaults to `http://172.17.0.2` |
| hass_host     | Hass API including scheme, defaults to `http://172.17.0.1:8123` |
| hass_key      | Hass API password  |
| hass_restart  | Flag indicating whether Hass restart desired, default to `true` | 
| notify        | Flat indicating whether notifications sending desired, defaults to `true` | 
| notify_entity | Name of entity which should be used for notifications, excluding `notify` |
| hass_watch    | List of folders or files used by Hass |
| addons        | List of object describing addons | 
| --> name      | Name of the addon | 
| --> watch     | Folder or file to watch |

> Be careful with schemas as nodejs handling http->https redirects very bad. 
So it's better use real schema without relaying on nginx proxy too much. 

### Logic 
Addon will perform `git pull` command and compare changes towards folders you've specified 
inside `hass_watch` and `addons`. If any of changed files are children to one of the folders, 
watcher will initiate restart of corresponding addon or HASS.

### Example config
```yaml
{
  "base_dir": "/config",
  "check_delay": 1,
  "hassio_host": "http://172.17.0.2",
  "hass_host": "http://172.17.0.1:8123",
  "hass_key": "PASSWORD",
  "notify": true,
  "notify_entity": "my_telegram",
  "hass_watch": [
    "config", 
    "configuration.yaml"
  ],
  "addons": [
    {
      "name": "AppDaemon",
      "watch": "hadaemon/dashboards"
    },
    {
      "name": "AppDaemon",
      "watch": "hadaemon/apps"
    }
  ]
}
```

Plese note, that `config` folder under `hass_watch` means that changes under `/config/config` 
will trigger hass restart and not just `/config`. 