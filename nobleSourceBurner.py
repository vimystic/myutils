from web3 import Web3
import bech32

def address_to_bech32(address, tag):
    if address == "":
        return ""
    address_bytes = bytes.fromhex(address)
    converted_bits = bech32.convertbits(address_bytes, 8, 5, True)
    if not converted_bits:
        raise ValueError("Error converting bits for Bech32 encoding.")
    bech32_address = bech32.bech32_encode(tag, converted_bits)
    return bech32_address

def process_transaction(tx_hash, tag='noble'):
    tx = w3.eth.get_transaction(tx_hash)
    input_data = tx.input
    hex_input_data = input_data.hex() if isinstance(input_data, bytes) else input_data
    if len(hex_input_data) < (133*2):
        return ""
    address_hex_str = hex_input_data[133*2:153*2]  
    bech32_address = address_to_bech32(address_hex_str, tag)
    return bech32_address

alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/2PZMX2BG8IFkT_l_923CtNPrXIIbtlxr"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check if web3 is successfully connected
# print("Connected to Ethereum network:", w3.is_connected())

# Function to read transaction hashes from a CSV file
def read_tx_hashes_from_csv(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        tx_hashes = data.split(',') 
    return tx_hashes

# File paths
file_paths = [
    '0xEF1a3C293875b8240F20d0Bbbb2461695Cd1E76d.csv',
    '0xf3cc88ff74833abc6c04ba39c62ea608a138eb3c.csv'
]

tx_hashes = []
for path in file_paths:
    tx_hashes.extend(read_tx_hashes_from_csv(path))

for tx_hash in tx_hashes:
    bech32_address = process_transaction(tx_hash.strip()) 
    print(f" {tx_hash}: {bech32_address}")
