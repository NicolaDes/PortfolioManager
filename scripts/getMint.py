import requests

url = "https://api-mainnet.magiceden.dev/v2/tokens/9Cx7uwD17UkRogEhep99y1sbbmjf1eqJ4vkHyKXHKjW8"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response)

print(response.text)