from typing import NamedTuple
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from time import sleep
import threading
from random import randint

class Asset(NamedTuple):
    symbol: str
    name: str
    hash: str
    amount_of_tokens: float
    contract_address: str

class NFTWebhook():
    def __init__(self):
        pass

    def personal_webhook(asset, ether_amount, wallet_address):
        if wallet_address == '0x504370ce2abef4ebea8c0aac33abdb30160e31e4':
            webhook = DiscordWebhook(
                url='https://discord.com/api/webhooks/997066333613195305/NEArXdxSQRIkCYBQUaPNjndzAOXIibU3mtmnw5dOo6ryxiiYSAGDoB22wn849mWkbK_d')  #big baller 2
        elif wallet_address == '0x1f2159afcb737510deb559a3baa5b6e5d79bae64':
            webhook = DiscordWebhook(
                url='https://discord.com/api/webhooks/997107188294230046/Bj-aajEdDodixiYkk1Fl9FQWgFbra3U0ytTVtLzZudZgZCV5L-LbcIlojaXDL6gHzUqW')  #less spammy
        elif wallet_address == '0x1f2159afcb737510deb559a3baa5b6e5d79bae64':
            webhook = DiscordWebhook(
                url='https://discord.com/api/webhooks/997107188294230046/Bj-aajEdDodixiYkk1Fl9FQWgFbra3U0ytTVtLzZudZgZCV5L-LbcIlojaXDL6gHzUqW')  #big baller  
        else:
            webhook = DiscordWebhook(
                url='https://discord.com/api/webhooks/996771713868111892/23PdREOHd-g8cm9NJp_qO2604XlT7AIHACo08_lVNJmPrMUWSI5-G7GTvQ_mQWTe3Fdc')    #anoth guy
        
        embed = DiscordEmbed(title=f"New Coin "+asset.name,color=2021216) 
        embed.set_thumbnail(url="https://etherscan.io/images/main/empty-token.png")
        embed.add_embed_field(name="ETH amount Of Buy | Number Of "+asset.symbol, value=str(ether_amount)+'    |    '+str(asset.amount_of_tokens), inline=False)
        embed.add_embed_field(name="Dextools Link", value=f"**[Link]("+'https://www.dextools.io/app/ether/pair-explorer/'+asset.contract_address+")**", inline=False)
        embed.add_embed_field(name="Symbol", value=asset.symbol, inline=True)
        embed.add_embed_field(name="Transaction Hash", value=asset.hash, inline=False)
        embed.add_embed_field(name="Wallet", value=f"**[Link]("+f'https://etherscan.io/address/{wallet_address}#tokentxns'+")**", inline=False) 
        embed.set_footer(text="Coin Monitors By Rob | " + str(datetime.now()))
        webhook.add_embed(embed)
        webhook.execute()

class NFShitCoins():
    def __init__(self,wallet_address):
        self.previuos_name = ['sdafsadf'] 
        self.wallet_address = wallet_address   
        self.api_key = "TE6WYYB3X7VWWIFAADREWTA2NQNPEFG4PI" 
        self.throttled = 0 
        self.scraper = requests.session()
        self.monitor()

    def parse_transactions(self,response):
        asset = Asset(
            symbol=response.json()["result"][0]["tokenSymbol"],
            name=response.json()["result"][0]["tokenName"],
            hash=response.json()["result"][0]["hash"],
            amount_of_tokens=int(response.json()["result"][0]["value"])/1000000000000000000,
            contract_address = response.json()["result"][0]["contractAddress"],
        )
        return asset


    def get_coin_transactions(self):
        return self.parse_transactions(self.scraper.get(f'https://api.etherscan.io/api?module=account&action=tokentx&address={self.wallet_address}&startblock=0&endblock=999999999&sort=desc&apikey={self.api_key}'))

    def parse_specific_transaction(self,response):
        return round(int(response.json()["result"]['value'], 16)/1000000000000000000,4)  

    def get_eth_value_of_transaction(self,asset):   
        return self.parse_specific_transaction(self.scraper.get(f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={asset.hash}&apikey={self.api_key}'))


    def monitor(self):
        print(f"[{str(datetime.now())}]  -> Monitoring")
        self.previuos_name = ['sdafsadf']
        while True:
            asset = self.get_coin_transactions()
            print(f"[{str(datetime.now())}]  -> Got Transactions")
            if asset.name in self.previuos_name:
                print(f"[{str(datetime.now())}]  -> Already Notified Coin: {asset.name} Waiting......")
                sleep(randint(3,15))
            else:
                eth_value = self.get_eth_value_of_transaction(asset)
                print(f"[{str(datetime.now())}]  -> Got ETH Value of Transaction")

                NFTWebhook.personal_webhook(asset, eth_value, self.wallet_address)
                print(f"[{str(datetime.now())}]  -> Notified Coin: {asset.name}")
                if len(self.previuos_name) == 2:
                    self.previuos_name.pop(0)
                self.previuos_name.append(asset.name)
                self.throttled = 0
                sleep(randint(3,30))


#wallets = ['0x079386dcf2f4b571b804112af97ff9d5ac2c538e','0xb0d6b433c850aa0afabed1532993866d7f7e507e','0x79979be80f16a7600297e0ce23d08d1a5e174aee','0x8722c7d5aa13e400016576eb634c1a1407805415','0x5cde4882124dc1d3ed475d3c162e7e08d7e510ba','0x3467eba885767d3ac9e754380036ab04d275942a']

wallets = ['0x504370ce2abef4ebea8c0aac33abdb30160e31e4','0xbcb05a3f85d34f0194c70d5914d5c4e28f11cc02','0x1f2159afcb737510deb559a3baa5b6e5d79bae64','0x8e533dbe7b12af95a398b687d9e1d5903be8c938','0x8b86dcfecf8afc02b6f6576afb057269c1e5ab90','0x7c6a40caaf66da1681fa2b424dc9346349cb8b9d','0x13b62e85b9c79a687463ce1fa462c23a7ae513b4','0x87549bda26c015e15fb3dd83aa34723a70d43ca7']

i = 0
for i in range(len(wallets)):
    x = threading.Thread(target=NFShitCoins, args=(wallets[i],))
    x.start()
    sleep(3)
