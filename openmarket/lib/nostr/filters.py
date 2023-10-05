from secrets import token_hex

class Filters:
    
    def __init__(self, ids: list = [], authors: list = [], kind: list = [], since: int = None, until: int = None, limit: int = 10) -> None:
        self.ids = ids
        self.kind = kind
        self.since = since
        self.until = until
        self.limit = limit
        self.authors = authors
            
    def make(self):
        event = {"limit": self.limit}
        if (self.ids):
            event["ids"] = self.ids
        
        if (self.kind):
            event["kind"] = self.kind
        
        if (self.authors):
            event["authors"] = self.authors
        
        if (self.since):
            event["since"] = self.since
        
        if (self.until):
            event["until"] = self.until
        
        return ["REQ", token_hex(6), event]
        
    