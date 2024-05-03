import requests
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc.types import TokenAccountOpts

# Inizializza il client RPC per connettersi al cluster Solana desiderato
solana_client = Client("https://api.mainnet-beta.solana.com")

# Sostituisci 'YOUR_ADDRESS' con l'indirizzo Solana di cui vuoi ottenere gli asset
address = '5J7UzwwZP1eWwE9UUrGxoPMnCYPr45jPhBRYo9xWYBKC'

# Prepara l'argomento 'opts'
opts = TokenAccountOpts(program_id=Pubkey.from_string('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'))

# Ottieni i saldi dei token per l'indirizzo specificato
response = solana_client.get_token_accounts_by_owner_json_parsed(Pubkey.from_string(address), opts)

# Controlla se la risposta ha un valore e poi accedi ai dati
if response.value is not None:
    for account_info in response.value:
        print(f"####### {account_info}")
        print(f"Indirizzo del token: {account_info.pubkey}")
        print(f"Saldo del token: {account_info.account.data.parsed['info']['tokenAmount']['uiAmount']}")

        url = "https://api.helius.xyz/v0/token-metadata"

        body = {
            'mintAccounts': [str(account_info.account.data.parsed['info']['mint'])]
        }

        print(f"body {body}")
        response = requests.post(url, json=body)

        if response.status_code == 200:
            print(f"data: {data}")
            data = response.json()
            token_symbol = data.get('symbol', 'Simbolo non trovato')
            print(f"Simbolo: {token_symbol}")
        else:
            print(f"Impossibile ottenere informazioni sul token con pubkey: {account_info.pubkey}")