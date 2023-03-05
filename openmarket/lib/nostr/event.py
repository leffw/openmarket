from secp256k1 import PrivateKey
from datetime import datetime
from hashlib import sha256
from time import time

import json

class EventKID:
    TEXT_NOTE = 1

class Event:
    
    def __init__(self, public_key: str, content: str, kind: int = EventKID.TEXT_NOTE, tags: list = [], created_at: int = int(time())):
        self.public_key = public_key
        self.created_at = created_at
        self.signature = None
        self.content = content
        self.tags = tags
        self.kind = kind
        self.id = Event.compute_id(
            public_key=self.public_key,
            content=self.content,
            kind=self.kind,
            tags=self.tags,
            created_at=self.created_at
        )

    @staticmethod
    def serialize(public_key: str, content: str, kind: int, tags: list, created_at: int) -> str:        
        return json.dumps([0, public_key, created_at, kind, tags, content], separators=(',', ':'), ensure_ascii=False)
    
    @staticmethod
    def compute_id(public_key: str, content: str, kind: int, tags: list, created_at: int) -> str:
        serialized = Event.serialize(public_key, content, kind, tags, created_at).encode()
        return sha256(serialized).hexdigest()
    
    def sign(self, private_key: str) -> str:
        sk = PrivateKey(bytes.fromhex(private_key))
        self.signature = sk.schnorr_sign(
            bytes.fromhex(self.id), None, raw=True).hex()
        return self.signature

    def to_dict(self):
        return {
            "id":         self.id,
            "pubkey":     self.public_key,
            "created_at": self.created_at,
            "kind":       self.kind,
            "tags":       self.tags,
            "content":    self.content,
            "sig":        self.signature
        }