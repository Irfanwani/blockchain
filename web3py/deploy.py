import os
from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# install_solc("0.8.15") # uncomment this line to install solidity version 0.8.15.

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.15",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# To deploy the cotract, we need to get the bytecode and abi of the contract

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# Ganache is a fake (simulated) blockchain which we are going to use for our project deployment.

#  connecting to rinkeby

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/9cc547604894475986c383c224141c42")
)
chain_id = 4
my_address = "0x954dC1202b3997e2785fCDfEcFfb52b5D591a26d"

private_key = os.getenv("private_key")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# now we need to build a transaction, then sign it and send it

# get latest trnsaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. build a transaction
# 2. sign the transaction
# 3. send the transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)

# send the signed transaction

tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)


# waiting till the transaction goes through
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)


# working with the contract (i.e, interacting with it). For that we need :
# contract address
# contract ABI
simple_storage = w3.eth.contract(address=tx_reciept.contractAddress, abi=abi)


# Two ways to interact with a transaction, call(simulate making a call and getting a return value i.e, they dont make any state changes) and transact (actually makes a state change)
print(
    simple_storage.functions.retrieve().call()
)  # will print the initial value of the number used in the simplestorage contract


print("creating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

print("signing contract...")
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)


print("sending the contract...")
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)

print("waiting for the contract to complete...")
tx_reciept = w3.eth.wait_for_transaction_receipt(send_store_tx)

print("Deployed!!!")
print(simple_storage.functions.retrieve().call())
