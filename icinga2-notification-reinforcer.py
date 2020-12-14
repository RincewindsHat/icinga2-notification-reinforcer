#!/usr/bin/env python3

import sys
import json

# Uncomment this if you wish to import the api library as ugly as me
#sys.path.append('/path/to/python-icinga2api/')

from icinga2api.client import Client

# Your URL here again
client  = Client('https://localhost:5665', config_file="./icinga2-api.conf")

states = {
        0 : "OK",
        1 : "WARNING",
        2 : "CRITICAL",
        3 : "UNKOWN"
        }

state_events = client.events.subscribe(["StateChange"], "state")

for i in state_events:
    json_stuff = json.loads(i)
    state_before = int(json_stuff["check_result"]["vars_before"]["state"])
    state_after = int(json_stuff["check_result"]["vars_after"]["state"])
    host = json_stuff["host"]
    if json_stuff["service"]:
        # Service problem
        service = json_stuff["service"]
        if (state_before == 1) and (state_after > state_before):
            client.actions.send_custom_notification("Service", filters=f'service.name=="{service}" && host.name=="{host}"', author="script", comment="dirty hack")
            print(f"Service {service} on Host {host} changed from {states[state_before]} to {states[state_after]}")
