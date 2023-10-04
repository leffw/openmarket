# MIP 1: Stupidly simple `DEX`

This document describes the creation of a communication protocol for a DEX that uses Nostr relays for the transmission and coordination of activities.

### Kids

- 123: Creation of the offer.
- 124: Take offer.
- 125: Accept offer.

## Creating offers

### Tags
- t: Type of order (e.g "SELL").
- r: Pair (e.g "BRL/BTC").
- v: Value.
- p: Price on sell.
- m: Payment method (e.g PIX, TED).
- x: Exchange public key.

```json
{
    "kid": 123,
    "tags": [
        ["t", "SELL"],
        ["r", "BRL/BTC"],
        ["v", "100000000"],
        ["p", "22393.63"],
        ["m", "PIX"],
        ["x", "94bf31181003df75c87f0914f37edde0095d403b1aeb7e38af91d5b09663ac57"]
    ]
}
```

## Take offer

### Tags

- i: Make offer id.

```json
{
    "kid": 124,
    "tags": [
        ["i", "47b142f9c09b1c9dfcbd44f4433e2f3f651d82cf544de78178b93c62b8312499"]
    ]
}
```

## Accept offer

- i: Take offer id

```json
{
    "kid": 125,
    "tags": [
        ["i", "6d13e15c3dd1f8f6501fced71d7c3e9f82bfc1737f0b0a85a6431b02644f7f49"]
    ],
}
```
