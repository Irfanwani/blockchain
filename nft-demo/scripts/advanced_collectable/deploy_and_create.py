import time
from scripts.helpful_scripts import fund_with_link, get_account
from brownie import AdvancedCollectable, config, network
from web3 import Web3


CONFIG = config["networks"][network.show_active()]

AMOUNT = Web3.toWei(3, "ether")

amt = Web3.toWei(1, "ether")


def main():
    account = get_account()

    advanced_collectable = AdvancedCollectable.deploy(
        CONFIG["vrf_coordinator"],
        CONFIG["link_token"],
        CONFIG["keyhash"],
        CONFIG["fee"],
        {"from": account},
        publish_source=True,
    )

    tx1 = fund_with_link(advanced_collectable.address, account, AMOUNT)
    tx1.wait(1)
    txn = advanced_collectable.topUpSubscription(amt, {"from": account})
    txn.wait(1)

    tx2 = advanced_collectable.addConsumer(
        advanced_collectable.s_subscriptionId(),
        advanced_collectable.address,
        {"from": account},
    )
    tx2.wait(1)

    tx = advanced_collectable.createCollectable(
        {"from": account},
    )
    tx.wait(1)
    time.sleep(300)

    print("New token has been created!")
