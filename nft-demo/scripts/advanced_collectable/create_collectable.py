import time

from brownie import AdvancedCollectable

from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()

    advanced_collectable = AdvancedCollectable[-1]

    

    tx = fund_with_link(
        advanced_collectable.address, account, amount=Web3.toWei(0.1, "ether")
    )

    tx.wait(1)

    create_txn = advanced_collectable.createCollectable({"from": account})

    create_txn.wait(3)

    print(advanced_collectable.s_subscriptionId())

    time.sleep(300)

    while not advanced_collectable.testInt():
        print(advanced_collectable.testInt())
        time.sleep(2)

    print("Collectable created")
