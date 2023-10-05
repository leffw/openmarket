# MIP 1: Stupidly Simple DEX

This document describes the creation of a communication protocol for a DEX that uses Nostr relays for the transmission and coordination of activities.

## Creating Offers

### Tags
- `#i`: Operation Identifier (1 Order Creation)
- `#t`: Type of order (e.g., "SELL").
- `#r`: Pair (e.g., "BRL/BTC").
- `#v`: Value.
- `#p`: Price on sell.
- `#m`: Payment method (e.g., PIX, TED).
- `#x`: Exchange public key.
- `#e`: Expiration

```json
{
    "kid": 1,
    "tags": [
        ["#i", "1"],
        ["#t", "SELL"],
        ["#r", "BRL/BTC"],
        ["#v", "10"],
        ["#p", "22393.63"],
        ["#m", "PIX"],
        ["#e", "3600"],
        ["#x", "94bf31181003df75c87f0914f37edde0095d403b1aeb7e38af91d5b09663ac57"]
    ]
}
```

## Take offer

### Tags

- `#i`: Operation Identifier (2 Order Take)
- `e`: Offer proposal id.
- `p`: Offer proposal pubkey.

```json
{
    "kid": 1,
    "tags": [
        ["e", "ed55257f93R0ce0cd99debcd4c7cd88f0c10857f2bf64402541fc3457fff46d1"],
        ["p", "6a974fa1d6c492794e9e75031dfe66329725b03fa096fb4785686d015930ded2"],
        ["#i", "2"],
        ["#x", "94bf31181003df75c87f0914f37edde0095d403b1aeb7e38af91d5b09663ac57"]
    ]
}
```

## Accept offer

### Tags
- `#i`: Operation Identifier (3 Order Accept)
- `e`: Offer proposal id.
- `p`: Offer proposal pubkey.

```json
{
    "kid": 1,
    "tags": [
        ["e", "ed55257f93R0ce0cd99debcd4c7cd88f0c10857f2bf64402541fc3457fff46d1"],
        ["p", "6a974fa1d6c492794e9e75031dfe66329725b03fa096fb4785686d015930ded2"],
        ["#i", "3"],
        ["#x", "94bf31181003df75c87f0914f37edde0095d403b1aeb7e38af91d5b09663ac57"]
    ]
}
```
