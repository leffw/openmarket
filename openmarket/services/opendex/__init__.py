from openmarket.lib.nostr.event import Event
from openmarket.lib.keychain import KeyChain

class OpenDex:
 
    @staticmethod
    def create(nsec: str, n: str, t: str, c: str, v: float, p: float, m: str, x: str) -> list:
        if not (n in ["BTC", "LNX"]):
            raise ValueError("Network is invalid.")
        
        if not (t in ["SELL", "BUY"]):
            raise ValueError("Type is invalid.")
        
        if not (c in ["BRL"]):
            raise ValueError("Currency is invalid.")
        
        if (v <= 0):
            raise ValueError("Value is invalid.")
        
        if (p <= 0):
            raise ValueError("Price is invalid.")
        
        if not (m in ["PIX"]):
            raise ValueError("Payment method is invalid.")
        
        if (x.startswith("npub") == True):
            x = KeyChain.from_npub(x).hex()
        
        npub = KeyChain.to_npub(nsec)

        # Create an offer creation event.  
        event = Event(
            npub,
            kind=123,
            tags=[
                ["n", n],
                ["t", t],
                ["c", c],
                ["v", str(v)],
                ["p", str(p)],
                ["m", m],
                ["x", x]
            ]
        )
        event.sign(nsec)
        return event.make()