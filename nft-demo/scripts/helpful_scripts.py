from brownie import accounts, config, network, interface, AdvancedCollectable

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        accounts.load(id)

    if (
        network.show_active()
        in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    account = accounts.add(config["wallets"]["from_key"])

    return account


def fund_with_link(address, account, amount):
    link_token = interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    )

    txn = link_token.transfer(address, amount, {"from": account})

    txn.wait(1)

    return txn


BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]
