from web3 import Web3
import bech32

def address_to_bech32(address, tag):
    print(address)
    if len(address) == 0:
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

alchemy_url = "hidden"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check if web3 is successfully connected
print("Connected to Ethereum network:", w3.is_connected())

# TODO : Import tx's from csv file and store in a list.
tx_hash = '0x1421274d360745b99a922b687e4516f7589e1eb999ddec9239daadf8a36f60cd'
print("Bech32 address:", process_transaction(tx_hash))
