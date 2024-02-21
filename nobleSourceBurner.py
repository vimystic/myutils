from web3 import Web3
import bech32
import json
import csv 

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
    address_hex_str = decode_function_input(contract, input_data)
    if address_hex_str == 'Error decoding input':
        return 'Error decoding transaction input'
    else:
        bech32_address = address_to_bech32(address_hex_str, tag)
        return bech32_address


def decode_function_input(contract, input_data):
    if input_data == '0x':
        return 'No data', {}
    try:
        func_obj, func_params = contract.decode_function_input(input_data)
        return (func_params['message']).hex()[-40:]
    except ValueError as e:
        print(f"Error decoding function input: {e}")
        return 'Error decoding input'


# Function to process transaction hashes from a CSV file
def process_tx_hashes_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        for row in reader:
            tx_hash = row[0].strip()  # Assumes the transaction hash is in the first column
            tx_hash_trimmed = tx_hash.strip()  
            bech32_address = process_transaction(tx_hash_trimmed)
            if bech32_address.startswith("Error"):
                print(f"Error processing transaction {tx_hash_trimmed}: {bech32_address}")
            else:
                print(f"Transaction {tx_hash_trimmed}: Bech32 address - {bech32_address}")


alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/2PZMX2BG8IFkT_l_923CtNPrXIIbtlxr"
w3 = Web3(Web3.HTTPProvider(alchemy_url))
with open('abi.json', 'r') as abi_definition:
    contract_abi = json.load(abi_definition)
contract_address = "0x0a992d191DEeC32aFe36203Ad87D7d289a738F81"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)



# Check if web3 is successfully connected
# print("Connected to Ethereum network:", w3.is_connected())

# File paths
file_paths = [
    '0xef.csv',
    '0xf3.csv'
]

for path in file_paths:
    process_tx_hashes_from_csv(path)
    

