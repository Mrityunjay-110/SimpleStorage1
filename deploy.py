from itertools import chain
import json
import os
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()
from solcx import compile_standard, install_solc
install_solc('0.8.15')


with open("./SimpleStorage.sol","r") as file:
    simple_storage_file=file.read()

compiled_sol=compile_standard({
    "language":"Solidity",
    "sources":{"SimpleStorage.sol":{"content":simple_storage_file}},
    "settings":{
        "outputSelection": {
            "*": {
                "*":["abi","metadata","evm.bytecode","evm.sourceMap"]
            }
        }
    },
},
solc_version="0.8.15",
)
with open("compiled_code.json","w") as file:
    json.dump(compiled_sol,file)

bytecode=compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi=compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3=Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id=1337
my_address="0x8FB41ee7F5317C0Bb9bf86f7ac3c3d858e36418f"
private_key=os.getenv("PRIVATE_KEY")


SimpleStorage=w3.eth.contract(abi=abi,bytecode=bytecode)

nonce=w3.eth.getTransactionCount(my_address)

transaction=SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice":w3.eth.gas_price,"chainId":chain_id,"from":my_address,"nonce":nonce
    }
)
signed_txn=w3.eth.account.sign_transaction(transaction,private_key=private_key)

tx_hash=w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt=w3.eth.wait_for_transaction_receipt(tx_hash)



simple_storage=w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)

print(simple_storage.functions.retrieve().call())
store_transaction=simple_storage.functions.store(15).build_transaction
(
    {
        "chainId":chain_id,"from":my_address,"nonce":nonce+1
    }
)
signed_store_txn=w3.eth.account.sign_transaction(
    store_transaction,private_key=private_key
)
send_store_tx=w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt=w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())
