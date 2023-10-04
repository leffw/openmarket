from openmarket.services.opendex import OpenDex
from openmarket.lib.keychain import KeyChain
from tabulate import tabulate
from os.path import exists
from glob import glob
from os import makedirs
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
@click.option("--exchange")
@click.option("--amount", required=True, type=int)
@click.option("--pair", required=True)
@click.option("--price", required=True, type=float)
@click.option("--payment-method", required=True)
def create_trade(operation: str, exchange: str, amount: int, pair: str, price: float, payment_method: str):
    if not exchange:
        exchange = configs["join"]

    # Create a trade order using OpenDex
    order = opendex.create(
        nsec=configs["nsec"],
        t=operation,
        r=pair,
        v=amount,
        p=price,
        m=payment_method,
        x=exchange
    )
    order_hex = binascii.hexlify(json.dumps(order).encode("utf-8")).decode()

    txid = order[-1]["id"]
    makedirs(f"./data/{exchange}", exist_ok=True)
    with open(f"./data/{exchange}/{txid}.hex", "w") as w:
        w.write(order_hex) 

    click.echo(f"Txid: {txid}")

# Command to list trade orders
@cli.command("book")
def list_trades():
    exchange = configs["join"]
    orders = {
        "BUY": [],
        "SELL": []
    }
    for path in glob(f"./data/{exchange}/*"):
        with open(path) as tx:
            tx = binascii.unhexlify(tx.read()).decode()
            tx = json.loads(tx)
            if not tx[0] == "EVENT":
                continue
            else:
                tx = tx[-1]
            
            tags = tx["tags"]
            txid = tx["id"]
            op = None
            tx = dict()
            for tag in tags:
                k, v = tag
                if k == "t":
                    tx["type"] = v
                    op = v
                elif k == "r":
                    tx["pair"] = v
                elif k == "v":
                    tx["value"] = v
                elif k == "p":
                    tx["price"] = v
                elif k == "m":
                    tx["method"] = v
            
            tx["txid"] = txid
            if op == "BUY":
                orders["BUY"].append([
                    txid[:8],
                    tx["type"],
                    tx["pair"],
                    tx["value"],
                    tx["price"],
                    tx["method"]
                ])        
            else:
                orders["SELL"].append([
                    txid[:8],
                    tx["type"],
                    tx["pair"],
                    tx["value"],
                    tx["price"],
                    tx["method"]
                ])    

    click.echo(tabulate(
        orders["BUY"], 
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
        orders["SELL"], 
        headers=[
            "Txid", 
            "Type", 
            "Pair", 
            "Value",
            "Price",
            "Method Payment"
        ]
    ))
