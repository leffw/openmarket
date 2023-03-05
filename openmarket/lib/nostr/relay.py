from websocket import create_connection
from json import dumps, loads

class Relay:
    
    def __init__(self, relay: str) -> None:
        self.relay = create_connection(relay)
    
    def send(self, event_type: int, event: dict) -> dict:
        if not (event_type in ["EVENT", "REQ", "CLOSE"]):
            raise ValueError(f"Event: {event_type} is invalid.")
        
        self.relay.send(dumps([event_type, event]))        
        return loads(self.relay.recv())
    
    def close(self):
        self.relay.close()