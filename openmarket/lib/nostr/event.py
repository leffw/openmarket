from openmarket.lib.keychain import KeyChain
from secp256k1 import PrivateKey, PublicKey
from datetime import datetime
from hashlib import sha256
from time import time

import json

class EventKID:
    TEXT_NOTE = 1

class Event:
    
    def __init__(self, npub_or_pubkey: str, content: str = "", kind: list = [EventKID.TEXT_NOTE], tags: list = [], created_at: int = int(time())):
        if (npub_or_pubkey.startswith("npub") == True):
            npub_or_pubkey = KeyChain.from_npub(npub_or_pubkey).hex()
        
        self.public_key = npub_or_pubkey
        self.created_at = created_at
        self.signature = None
        self.content = content
        self.kind = kind
        self.tags = tags
        self.id = Event.compute_id(
            public_key=self.public_key,
            content=self.content,
            kind=self.kind,
            tags=self.tags,
            created_at=self.created_at
        )

    @staticmethod
    def serialize(public_key: str, content: str, kind: list, tags: list, created_at: int) -> str:        
        data = [0, public_key, created_at, kind, tags, content]
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    
    @staticmethod
    def compute_id(public_key: str, content: str, kind: int, tags: list, created_at: int) -> str:
        serialized = Event.serialize(public_key, content, kind, tags, created_at).encode()
        return sha256(serialized).hexdigest()
    
    def sign(self, nsec: str) -> str:
        sk = PrivateKey(KeyChain.from_nsec(nsec)) #bytes.fromhex(private_key))
        self.signature = sk.schnorr_sign(
            bytes.fromhex(self.id), None, raw=True).hex()
        return self.signature
    
    def verify(self) -> bool:
        pk = PublicKey(bytes.fromhex("02" + self.public_key), True)
        return pk.schnorr_verify(bytes.fromhex(self.id), bytes.fromhex(self.signature), None, raw=True)
    
    def make(self):
        return ["EVENT", {
            "id":         self.id,
            "pubkey":     self.public_key,
            "created_at": self.created_at,
            "kind":     self.kind,
            "tags":       self.tags,
            "content":    self.content,
            "sig":        self.signature
        }]