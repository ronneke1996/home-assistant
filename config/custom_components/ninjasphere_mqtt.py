from homeassistant.components.switch.demo import DemoSwitch
from homeassistant.core import State
import homeassistant.loader as loader
import homeassistant.const as const
import sys

sys.path.insert(0,"/home/simon/GitHub/Stash/pyninjasphere/")

import pyninjasphere
from pyninjasphere.services.service import Service

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "ninjasphere_mqtt"

# List of component names (string) your component depends upon.
DEPENDENCIES = ['mqtt']

DEFAULT_TOPIC = 'home-assistant/ninjasphere_mqtt'

def setup(hass, config):
	"""Setup the Hello MQTT component."""
	print("Loading the Ninja Sphere's things...")
	
	# Create the mqtt object
	mqtt = loader.get_component('mqtt')
	
	# Read all required variables from the config
	ip = config[DOMAIN].get('ip', DEFAULT_TOPIC)
	port_mqtt = config[DOMAIN].get('port_mqtt', DEFAULT_TOPIC)
	port_http = config[DOMAIN].get('port_http', DEFAULT_TOPIC)
	
	# Create the node and get the things from it
	node = Service(ip,port_mqtt, port_http)
	things = node.get_all_things()
	
	for thing in things:
		# Set the topic
		topic = "$device/"+str(thing.id)+"/#"
		
		# Set the entity id
		entity_id = thing.type+"."+thing.name.replace(" ", "_").replace(".","").replace("-","").replace("\\","").lower()
		
		# Add the entity to the Home Assistant GUI
		attributes = {"platform" : "mqtt",  "assumed_state" : True , "name" : thing.name, "state_topic" :  topic, "command_topic" : topic, "payload_on:" : "ON", "payload_off" : "OFF", "optimistic" : False, "qos" : 0, "retain" : True, "value_template" : "{{ value.x }}"}
		
		hass.states.set(entity_id,  "No channels", attributes)
		
		for channel in thing.device["channels"]:
			try:
				hass.states.set(entity_id,  channel["lastState"]["payload"], attributes)
				break
			except TypeError:
				hass.states.set(entity_id,  "No states", attributes)
				

		# Listener to be called when we receive a message.
		def message_received(topic, payload, qos):
			"""A new MQTT message has been received."""
			hass.states.set(entity_id, payload)

		# Subscribe our listener to a topic.
		mqtt.subscribe(hass, topic, message_received)

		# Service to publish a message on MQTT.
		def set_state_service(call):
			"""Service to send a message."""
			print("MQTT Message Sending...")
			mqtt.publish(hass, topic, call.data.get('new_state'))

		# Register our service with Home Assistant.
		hass.services.register(DOMAIN, 'set_state', set_state_service)
	
	# Return boolean to indicate that initialization was successfully.
	return True
