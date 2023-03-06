from openmarket.lib.nostr import relay
from openmarket.configs import NOSTR_RELAY

import logging

relay = relay.Relay(NOSTR_RELAY)

def subscribe(filters: list, callback: object = None):
    relay.send(filters)
    
    while True:
        data = relay.recv()
        if not isinstance(data, list):
            continue
        
        if (len(data) == 0):
            continue
        
        if (data[0] != "EVENT"):
            continue
        
        logging.info(str(data))
        if (callback):
            callback(data)
            
    relay.close(id=filters[1])