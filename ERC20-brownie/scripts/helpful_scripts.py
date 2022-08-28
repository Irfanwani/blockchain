from brownie import network, accounts, config

LOCAL = ['development', 'mainnet-fork']

def get_account():
    if network.show_active() in LOCAL:
        return accounts[0]
    
    account = accounts.add(config['wallets']['from_key'])

    return account