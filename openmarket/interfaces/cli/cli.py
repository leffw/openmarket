from openmarket.services.opendex import OpenDex
from openmarket.services.nostr import relay
from openmarket.lib.keychain import KeyChain
from tabulate import tabulate
from os.path import exists

from time import time
from glob import glob
from os import makedirs, remove, rmdir

import binascii
import click
import json

# Initialize a KeyChain object
keychain = KeyChain()

# Create a directory './data' if it doesn't exist
makedirs("./data", exist_ok=True)

# If the wallet file doesn't exist, create it with default values
if not exists("./data/wallet.json"):
    with open("./data/wallet.json", "w") as w:
        json.dump({"nsec": None, "npub": None}, w)

# Load wallet configurations from the JSON file
with open("./data/wallet.json", "r") as r:
    configs = json.load(r)

# Create an OpenDex object
opendex = OpenDex()

# Define the CLI commands using Click
@click.group()
def cli():
    ...

# Command to create a new wallet
@cli.command("create")
def create_wallet():
    m = keychain.to_mnemonic()
    click.echo(f"Write the words on paper [{len(m.split())}]: {m}")

# Command to recover a wallet using a mnemonic phrase
@cli.command("recovery")
@click.argument("words")
def recovery_wallet(words: str):
    seed = keychain.to_seed(words)
    nsec = keychain.to_nsec(seed)
    npub = keychain.to_npub(nsec)
    
    # Update wallet configurations and save to the JSON file
    with open("./data/wallet.json", "w") as w:
        configs.update({
            "nsec": nsec,
            "npub": npub
        })
        w.write(json.dumps(configs))
    
    click.echo(f"Wallet recovered: {npub}")

# Command to set the exchange address to join
@cli.command("join")
@click.argument("npub")
def join_exchange(npub: str):
    # Update the exchange address and save to the JSON file
    with open("./data/wallet.json", "w") as w:
        configs.update({
            "join": npub,
        })
        w.write(json.dumps(configs))
    
    click.echo(f"Join: {npub}")

# Command to create a trade order
@cli.command("trade")
@click.option("--operation", required=True, type=click.Choice(['BUY', 'SELL']))
@click.option("--description", default="")
@click.option("--exchange")
@click.option("--amount", required=True, type=int)
@click.option("--pair", required=True)
@click.option("--price", required=True, type=float)
@click.option("--payment-method", required=True)
def create_trade(
        operation: str, 
        description: str,
        exchange: str, 
        amount: int, 
        pair: str, 
        price: float, 
        payment_method: str
    ):
    if not exchange:
        exchange = configs["join"]

    # Create a trade tx using OpenDex
    expiry_at = int((60 * 60) * 2)
    tx = opendex.create(
        nsec=configs["nsec"],
        d=description,
        t=operation,
        r=pair,
        v=amount,
        p=price,
        m=payment_method,
        x=exchange,
        e=expiry_at
    )
    tx_hex = binascii.hexlify(
        json.dumps(tx).encode("utf-8")).decode()

    txid = tx[-1]["id"]
    path = f"./data/{exchange}/{txid}"

    makedirs(f"{path}/proposals", exist_ok=True)
    with open(f"{path}/index.hex", "w") as w:
        w.write(tx_hex)

    click.echo(json.dumps({
        "txid": txid,
        "hex": tx_hex,
        "raw": json.dumps(tx),
        "relay": json.dumps(relay.send(tx))
    }, indent=3))

@cli.command("take")
@click.argument("txid")
@click.argument("pubk")
def take_trade(txid: str, pubk: str):
    tx = opendex.take(configs["nsec"], txid, pubk, configs["join"])
    tx_hex = binascii.hexlify(json.dumps(tx).encode("utf-8")).decode()
    with open(f"./data/" + \
            configs["join"] + \
                f"/{txid}/proposals/" + \
                    tx[-1]["id"] + ".hex", "w") as w:
        w.write(tx_hex)

    click.echo(json.dumps({
        "txid": txid,
        "hex": tx_hex,
        "raw": json.dumps(tx),
        "relay": json.dumps(relay.send(tx))
    }, indent=3))

@cli.command("accept")
@click.argument("order")
@click.argument("txid")
@click.argument("pubk")
def accept_trade(order: str, txid: str, pubk: str):
    tx = opendex.accept(
        configs["nsec"],
        txid,
        pubk,
        configs["join"]
    )
    tx_hex = binascii.hexlify(json.dumps(tx).encode("utf-8")).decode()
    with open(f"./data/" + \
            configs["join"] + \
                f"/{order}" + "accept.hex", "w") as w:
        w.write(tx_hex)

    rmdir("./data/" + configs["join"] + f"/{order}/proposals")

    click.echo(json.dumps({
        "txid": txid,
        "hex": tx_hex,
        "raw": json.dumps(tx),
        "relay": json.dumps(relay.send(tx))
    }, indent=3))

@cli.command("book")
def list_trades():
    txs = { "BUY": [], "SELL": [] }
    for path in glob(f"./data/" + configs["join"] + "/*/index.hex"):
        with open(path) as tx:
            tx = binascii.unhexlify(tx.read()).decode()
            tx = json.loads(tx)
            if not tx[0] == "EVENT":
                continue
            else:
                tx = tx[-1]

            created_at = tx["created_at"] 
            tags = tx["tags"]
            txid = tx["id"]
            op = None
            tx = dict()
            for tag in tags:
                k, v = tag
                if k == "#t":
                    tx["type"] = v
                    op = v
                elif k == "#r":
                    tx["pair"] = v
                elif k == "#v":
                    tx["value"] = v
                elif k == "#p":
                    tx["price"] = v
                elif k == "#m":
                    tx["method"] = v
                elif k == "#e":
                    tx["expiry_at"] = float(v)

            expiry_at = created_at + tx["expiry_at"]
            if time() >= expiry_at:
                remove(path)
                continue

            tx["txid"] = txid
            if op == "BUY":
                txs["BUY"].append([
                    txid[:16],
                    tx["type"],
                    tx["pair"],
                    tx["value"],
                    tx["price"],
                    tx["method"]
                ])        
            else:
                txs["SELL"].append([
                    txid[:16],
                    tx["type"],
                    tx["pair"],
                    tx["value"],
                    tx["price"],
                    tx["method"]
                ])    

    click.echo(tabulate(
        txs["BUY"], 
        headers=[
            "Txid", 
            "Type", 
            "Pair", 
            "Value",
            "Price",
            "Method Payment"
        ]
    ))

    click.echo("\n")

    click.echo(tabulate(
        txs["SELL"], 
        headers=[
            "Txid", 
            "Type", 
            "Pair", 
            "Value",
            "Price",
            "Method Payment"
        ]
    ))
