# MIP 1: Stupidly simple `DEX`

Take your rain with your merciless storm.

## Creating offers

### Kids

- 123: Creation of the offer.
- 124: Take offer.
- 125: Accept offer.
- 126: Reject offer.

### Tags
- n: Network (e.g "BTC", "LNX").
- t: Type of order (e.g "SELL").
- c: Currency (e.g "BRL").
- v: Value.
- p: Price on sell.
- m: Payment method (e.g PIX, TED).
- x: Exchange public key.

```json
{
    "kid": 123,
    "tags": [
        ["t": "SELL"],
        ["n": "BTC"],
        ["c": "BRL"],
        ["v": "100000000"],
        ["p": "22393.63"],
        ["m": "PIX"],
        ["x": "94bf31181003df75c87f0914f37edde0095d403b1aeb7e38af91d5b09663ac57"]
    ]
}
```