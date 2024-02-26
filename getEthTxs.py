import requests
import datetime

def fetch_eth_price_for_date(date, api_key):
    base_url = "https://api.etherscan.io/api"
    params = {
        "module": "stats",
        "action": "ethdailyprice",
        "startdate": date.strftime('%Y-%m-%d'),
        "enddate": date.strftime('%Y-%m-%d'),
        "sort": "asc",
        "apikey": api_key
    }
    response = requests.get(base_url, params=params)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == '1' and data.get('result'):
            price_info = data['result'][0]  
            return float(price_info['value'])
        else:
            return "No data available for the specified date."
    else:
        return "Failed to fetch the ETH price."

API_KEY = 'XERDNHTZC4SBRY5VWMUXQ5Z7RPNUGB428P'
ADDRESS = '0xf3cc88ff74833abc6c04ba39c62ea608a138eb3c'

now = datetime.datetime.now()
today_price = fetch_eth_price_for_date(now, API_KEY)
yesterday = now - datetime.timedelta(days=1)
yesterday_price = fetch_eth_price_for_date(yesterday, API_KEY)
print(f"Today's ETH price: {today_price}")
print(f"Yesterday's ETH price: {yesterday_price}")

url = f"https://api.etherscan.io/api?module=account&action=txlist&address={ADDRESS}&startblock=0&endblock=99999999&sort=desc&apikey={API_KEY}"

response = requests.get(url)
data = response.json()

one_day_ago = now - datetime.timedelta(days=1)
recent_transactions = [
    tx for tx in data['result'] if datetime.datetime.fromtimestamp(int(tx['timeStamp'])) > one_day_ago
]

if 'result' in data and isinstance(data['result'], list):
    for tx in recent_transactions:
        if isinstance(tx, dict):
            tx_timestamp = datetime.datetime.fromtimestamp(int(tx['timeStamp']))
            eth_price = today_price if tx_timestamp.date() == now.date() else yesterday_price
            tx_hash = tx['hash']
            tx_fee_eth = (int(tx['gasUsed']) * int(tx['gasPrice'])) / 1e18  # Convert Wei to Ether
            print(f"{tx_hash}, {tx_timestamp}, {tx_fee_eth:.18f}, {eth_price}")
else:
    print("Error: Unexpected response format.")
