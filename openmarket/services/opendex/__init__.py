from openmarket.lib.nostr.filters import Filters
from openmarket.lib.nostr.event import Event
from openmarket.lib.keychain import KeyChain
from time import time

class OpenDex:
 
    @staticmethod
    def create(nsec: str, d: str, t: str, r: str, v: float, p: float, m: str, x: str, e: int) -> list:
        if not (t in ["SELL", "BUY"]):
            raise ValueError("Type is invalid.")

        if (v <= 0):
            raise ValueError("Value is invalid.")
        
        if (p <= 0):
            raise ValueError("Price is invalid.")
        
        if not (m in ["PIX"]):
            raise ValueError("Payment method is invalid.")
        
        if x.startswith("npub"):
            x = KeyChain.from_npub(x).hex()

        created_at = int(time())
        content = (
            f"[{t}]({r})\n\n"
            f"Exchange: {x}\n"
            f"Expires in: {e + created_at}\n\n"
            f"Value: {v}\n"
            f"Price: {p}\n"
            f"Payment method: {m}\n\n"
            f"{d}"
        )
        npub = KeyChain.to_npub(nsec)
        event = Event(
            npub,
            content=content,
            kind=1,
            tags=[
                ["#i", "1"],
                ["#t", str(t)],
                ["#r", str(r)],
                ["#v", str(v)],
                ["#p", str(p)],
                ["#m", str(m)],
                ["#x", x],
                ["#e", str(e)]
            ],
            created_at=created_at
        )
        event.sign(nsec)
        return event.make()

    @staticmethod
    def take(nsec: str, e: str, p: str, x: str) -> list:
        npub = KeyChain.to_npub(nsec)
        content = (
            "[Take]\n\n"
            f"Exchange: {x}\n"
            f"ID: {e[:16]}\n"
        )
        event = Event(
            npub,
            content=content,
            kind=1,
            tags=[
                ["e", e],
                ["p", p],
                ["#i", "2"],
                ["#x", x]
            ]
        )
        event.sign(nsec)
        return event.make()

    @staticmethod
    def accept(nsec: str, e: str, p: str, x: str) -> list:
        npub = KeyChain.to_npub(nsec)
        content = (
            "[Accept]\n\n"
            f"Exchange: {x}\n"
            f"ID: {e[:16]}\n"
        )
        event = Event(
            npub,
            content=content,
            kind=1,
            tags=[
                ["e", e],
                ["p", p],
                ["#i", "3"],
                ["#x", x]
            ]
        )
        event.sign(nsec)
        return event.make()
