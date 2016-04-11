"""
Support for NinjaSphere.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/ninjasphere/
"""
import logging

# Import the device class
from homeassistant.const import CONF_HOST

REQUIREMENTS = ['pyninjasphere==0.0.1.dev0']

DOMAIN = "ninjasphere"

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Initialize NinjaSphere platform."""

    # Validate passed in config
    host = config.get(DOMAIN, CONF_HOST)[CONF_HOST]

    if host is None:
        _LOGGER.error('Invalid config. Expected %s', CONF_HOST)
        return False

    _LOGGER.info('host %s', host)
    _LOGGER.info('host is a %s', type(host))

    from pyninjasphere.things import Node

    node = Node(host)
    things = node.get_all_things()
    _LOGGER.info('Created a host and called things %s', things)

    return True
