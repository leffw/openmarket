# OpenMarket
A simple DEX protocol based on Lightning
and Nostr

## How to Install?
Run the following command to install Python 3 and the 
Python pip package manager:

```bash
sudo apt-get install python3 python3-pip
pip3 install poetry
poetry install
```

## How to Create a New Wallet?

To create a new wallet, you can use the following command:

```bash
poetry run cli create 

Write the words on paper [24]: phrase exist unusual fame river select fit refuse modify guide fun father old easy exercise bind rubber beef scout spice pulse penalty flash since
```

## How to Recover a Wallet?

If you already have a mnemonic phrase, you can recover your wallet 
using the following command:
```bash
poetry run cli recovery "phrase exist unusual fame river select fit refuse modify guide fun father old easy exercise bind rubber beef scout spice pulse penalty flash since"
```
Replace "Words" with your own mnemonic phrase.

## How to Join an Exchange?
To join an exchange, you can use the following command:

```bash
poetry run cli join npub1zks4p228gncmqdskml0n8fvfeguyqp8xrht29kt6kh2swsmzdgyqx46anu
```
Replace npub1zks4p228gncmqdskml0n8fvfeguyqp8xrht29kt6kh2swsmzdgyqx46anu with the address of the desired exchange.

## How to Create a New Trade Order?

```bash
poetry run cli trade --operation BUY --amount 10 --pair BTC/BRL --price 142975 --payment-method PIX
```
```bash
Txid: 6b43f7dc980b10583fcf1b453ac621b2670ca0a83dae9b92055d14cecb7f4477
```

## How to List All Trade Orders on the Exchange?
To list all trade orders on the exchange, you can use the following command:

```bash
$ poetry run cli book
```
```bash
Txid      Type    Pair       Value    Price  Method Payment
--------  ------  -------  -------  -------  ----------------
6b43f7dc  BUY    BTC/BRL       10   142975  PIX
```