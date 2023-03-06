from websocket import create_connection
from json import dumps, loads

class Relay:
    
    def __init__(self, relay: str) -> None:
        self.relay = create_connection(relay)
    
    def send(self, event: list, no_recv=False) -> dict:
        self.relay.send(dumps(event))
        if (no_recv == False):
            return self.recv()
        else:
            return {}

    def recv(self) -> dict:
        return loads(self.relay.recv())
        
    def close(self, id: str = None) -> None:
        if (id):
            self.send(dumps(["CLOSE", id]))
        
        try:
            self.relay.close()
        except:
            pass
    