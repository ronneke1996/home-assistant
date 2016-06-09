import homeassistant.components.light as light


class Light(dict):
    """ Class for creating a Light from a light-thing. """

    def __init__(self, thing):
        self.parse_light_from_thing(thing)

    def add_field(self, key, item):
        self.__setitem__(key, item)

    def parse_light_from_thing(self, thing):
        self.add_field('platform', 'mqtt')
        for channel in thing.device.channels:
            if channel.protocol == 'on-off':
                self.add_field('name', thing.device.name + " " + channel.id)
                self.add_field('state_topic', channel.topic)
                self.add_field('command_topic', channel.topic)
                self.add_field(
                    'payload_on', self.payload_constructor('turnOn'))
                self.add_field(
                    'payload_off', self.payload_constructor('turnOff'))
            elif channel.protocol == 'brightness':
                self.add_field('brightness_state_topic', channel.topic)
                self.add_field('brightness_command_topic', channel.topic)
                self.add_field('payload_brightness', self.payload_constructor(
                    'set', 'placeholder_brightness'))
                self.add_field('brightness_value_template',
                               '{{ value_json.params[0] }}')

    def payload_constructor(self, method, params=""):
        return '{\"method\": \"' + method + '\",\"params\":['\
               + params + '],\"id\":\"123\",\"jsonrpc\":\"2.0\"}'
