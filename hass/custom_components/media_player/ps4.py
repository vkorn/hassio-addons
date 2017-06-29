"""Playstation 4 media_player using ps4-waker."""
import json
import logging
from datetime import timedelta
from urllib.parse import urlparse
import requests
import voluptuous as vol

import homeassistant.util as util
from homeassistant.components.media_player import (
    PLATFORM_SCHEMA,
    MEDIA_TYPE_CHANNEL,
    SUPPORT_TURN_ON,
    SUPPORT_TURN_OFF,
    SUPPORT_STOP,
    SUPPORT_SELECT_SOURCE,
    ENTITY_IMAGE_URL,
    MediaPlayerDevice
)
from homeassistant.const import (
    STATE_IDLE,
    STATE_UNKNOWN,
    STATE_OFF,
    STATE_PLAYING,
    CONF_NAME,
    CONF_HOST
)
from homeassistant.helpers import config_validation as cv

REQUIREMENTS = []

_LOGGER = logging.getLogger(__name__)

SUPPORT_PS4 = SUPPORT_TURN_OFF | SUPPORT_TURN_ON | \
              SUPPORT_STOP | SUPPORT_SELECT_SOURCE

DEFAULT_NAME = 'Playstation 4'
DEFAULT_PORT = ''
ICON = 'mdi:playstation'
CONF_GAMES_FILENAME = 'games_filename'
CONF_IMAGEMAP_JSON = 'imagemap_json'
CONF_CMD = 'cmd'
CONF_LOCAL_STORE = "local_store"
CONF_PS4_IP = "ps4_ip"

PS4_GAMES_FILE = 'ps4-games.json'
MEDIA_IMAGE_DEFAULT = None
MEDIA_IMAGEMAP_JSON = 'https://github.com/hmn/ps4-imagemap/raw/master/games.json'
LOCAL_STORE = None

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=10)
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PS4_IP): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_GAMES_FILENAME, default=PS4_GAMES_FILE): cv.string,
    vol.Optional(CONF_IMAGEMAP_JSON, default=MEDIA_IMAGEMAP_JSON): cv.string,
    vol.Optional(CONF_LOCAL_STORE, default=LOCAL_STORE): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup PS4 platform."""
    if discovery_info is not None:
        ip = urlparse(discovery_info[1]).hostname
    else:
        ip = config.get(CONF_PS4_IP)

    if ip is None:
        _LOGGER.error("No PS4 found in configuration file or with discovery")
        return False

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    games_filename = hass.config.path(config.get(CONF_GAMES_FILENAME))
    games_map_json = config.get(CONF_IMAGEMAP_JSON)
    local_store = config.get(CONF_LOCAL_STORE)

    ps4 = PS4Waker(host, ip, games_filename)
    add_devices([PS4Device(name, ps4, games_map_json, local_store)], True)


class PS4Device(MediaPlayerDevice):
    """Representation of a PS4."""

    def __init__(self, name, ps4, gamesmap_json, local_store):
        """Initialize the ps4 device."""
        self.ps4 = ps4
        self._name = name
        self._state = STATE_UNKNOWN
        self._media_content_id = None
        self._media_title = None
        self._current_source = None
        self._current_source_id = None
        self._games_map_json = gamesmap_json
        self._games_map = {}
        self._local_store = local_store
        if self._local_store is None:
            self.load_games_map()
        self.update()

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def update(self):
        """Retrieve the latest data."""
        data = self.ps4.search()
        self._media_title = data.get('running-app-name')
        self._media_content_id = data.get('running-app-titleid')
        self._current_source = data.get('running-app-name')
        self._current_source_id = data.get('running-app-titleid')

        if data.get('status') == 'Ok':
            if self._media_content_id is not None:
                self._state = STATE_PLAYING
            else:
                self._state = STATE_IDLE
        else:
            self._state = STATE_OFF
            self._media_title = None
            self._media_content_id = None
            self._current_source = None
            self._current_source_id = None

    def load_games_map(self):
        try:
            self._games_map = json.loads(requests.get(self._games_map_json, verify=False))
        except Exception as e:
            _LOGGER.error("gamesmap json file could not be loaded, %s" % e)

    @property
    def entity_picture(self):
        if self.state == STATE_OFF:
            return None

        if self._local_store is None:
            image_hash = self.media_image_hash

            if image_hash is None:
                return None

            return ENTITY_IMAGE_URL.format(
                self.entity_id, self.access_token, image_hash)

        if self._media_content_id is None:
            return None

        filename = "/local/%s/%s.jpg" % (self._local_store, self._media_content_id)
        return filename

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def icon(self):
        """Icon."""
        return ICON

    @property
    def media_content_id(self):
        """Content ID of current playing media."""
        return self._media_content_id

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        return MEDIA_TYPE_CHANNEL

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        if self._media_content_id is None:
            return MEDIA_IMAGE_DEFAULT
        try:
            return self._games_map[self._media_content_id]
        except KeyError:
            return MEDIA_IMAGE_DEFAULT

    @property
    def media_title(self):
        """Title of current playing media."""
        return self._media_title

    @property
    def supported_features(self):
        """Media player features that are supported."""
        return SUPPORT_PS4

    @property
    def source(self):
        """Return the current input source."""
        return self._current_source

    @property
    def source_list(self):
        """List of available input sources."""
        return sorted(self.ps4.games.values())

    def turn_off(self):
        """Turn off media player."""
        self.ps4.standby()

    def turn_on(self):
        """Turn on the media player."""
        self.ps4.wake()
        self.update()

    def media_pause(self):
        """Send keypress ps to return to menu."""
        self.ps4.remote('ps')
        self.update()

    def media_stop(self):
        """Send keypress ps to return to menu."""
        self.ps4.remote('ps')
        self.update()

    def select_source(self, source):
        """Select input source."""
        for titleid, game in self.ps4.games.items():
            if source == game:
                self.ps4.start(titleid)
                self._current_source_id = titleid
                self._current_source = game
                self._media_content_id = titleid
                self._media_title = game
                self.update()


class PS4Waker(object):
    """Rest client for handling the data retrieval."""

    def __init__(self, url, ip, games_filename):
        """Initialize the data object."""
        self._url = url
        self._ip = ip
        self._games_filename = games_filename
        self.games = {}
        self._load_games()

    def __call(self, command, param=None):
        url = '{0}/ps4/{1}/{2}'.format(self._url, self._ip, command)
        if param is not None:
            url += '/{0}'.format(param)

        try:
            response = requests.get(url, verify=False)
            if 200 != response.status_code:
                raise Exception(response.text)
            return response.text
        except Exception as e:
            _LOGGER.error('Failed to call %s: %s', command, e)
            return None

    def _load_games(self):
        try:
            with open(self._games_filename, 'r') as f:
                self.games = json.load(f)
                f.close()
        except FileNotFoundError:
            self._save_games()
        except ValueError as e:
            _LOGGER.error('Games json file wrong: %s', e)

    def _save_games(self):
        try:
            with open(self._games_filename, 'w') as f:
                json.dump(self.games, f)
                f.close()
        except FileNotFoundError:
            pass

    def wake(self):
        """Wake PS4 up."""
        return self.__call('on')

    def standby(self):
        """Set PS4 into standby mode."""
        return self.__call('off')

    def start(self, title_id):
        """Start game using titleId."""
        return self.__call('start', title_id)

    def remote(self, key):
        """Send remote key press."""
        return self.__call('key', key)

    def search(self):
        """List current info."""
        value = self.__call('info')

        if value is None:
            return {}

        try:
            data = json.loads(value)
        except json.decoder.JSONDecodeError as e:
            _LOGGER.error("Error decoding ps4 json : %s", e)
            data = {}

        """Save current game"""
        if data.get('running-app-titleid'):
            if data.get('running-app-titleid') not in self.games.keys():
                game = {data.get('running-app-titleid'):
                            data.get('running-app-name')}
                self.games.update(game)
                self._save_games()

        return data
