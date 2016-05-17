import homeassistant.components.light as light
import homeassistant.components.media_player as media_player
from .ninjasphere_components.light import Light
from .ninjasphere_components.mediaplayer import MediaPlayer
from .ninjasphere_components.unknownthing import UnknownThing

import pyninjasphere.services.service as service

# The domain of this component. This one's equal to the name of this component.
DOMAIN = 'ninjasphere'

# List of component names (string) this component depends upon.
DEPENDENCIES = ['mqtt']

DEFAULT_TOPIC = 'home-assistant/ninjasphere'
DEFAULT_IP = '127.0.0.1'
DEFAULT_HTTP_PORT = '80'


def setup(hass, config):
    """
    Sets up the Ninja Sphere component
    """

    # TODO:Config validation
    # Read all required variables from the config
    ip = config[DOMAIN].get('ip', DEFAULT_IP)
    port_http = config[DOMAIN].get('http_port', DEFAULT_HTTP_PORT)

    # Create the node and get the things from it
    node = service.Service(ip, htpp_port=port_http)
    things = node.get_all_things()

    parse_things(hass, things)

    # Return boolean to indicate that initialization was successfully.
    print('Setup for component' + DOMAIN + ' succesful!')
    return True


def parse_things(hass, things):
    """
    Create lists for all different kinds of things
    """
    lights = []
    media_players = []

    for thing in things:        
        # Mediaplayer is found
        if thing.type == 'mediaplayer':
            media_players.append(MediaPlayer(thing))

        # Light is found
        elif thing.type == 'light':
            lights.append(Light(thing))

        # An unknown thing has been found
        else:
            UnknownThing(hass, thing)
        
    # Create configs
    light_config = {'light': lights}
    media_player_config = {'media_player': media_players}

    # Run setups of things
    light.setup(hass, light_config)
    media_player.setup(hass, media_player_config)
