from openmarket.lib.nostr import relay
from openmarket.configs import NOSTR_RELAY

import logging

relay = relay.Relay(NOSTR_RELAY)

def subscribe(filters: list, callback: object = None):
    relay.send(filters, no_recv=True)
    
    while True:
        data = relay.recv()
        logging.info(str(data))
        
        if not isinstance(data, list):
            continue
        
        if (len(data) == 0):
            continue
        
        if (data[0] != "EVENT"):
            continue
        
        if (callback):
            callback(data)
        
    relay.close(id=filters[1])