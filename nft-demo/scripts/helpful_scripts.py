from brownie import accounts, config, network

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        accounts.load(id)
    
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]

    account = accounts.add(config['wallets']['from_key'])

    return account
