from scripts.helpful_scripts import get_account
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    # Mints WETH by depositing ETH
    # ABI and address
    account = get_account()
    weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])

    tx = weth.deposit({'from': account, 'value': 0.1 * 10 ** 18})
    tx.wait(1)

    print('recieved 0.1 WETH')

    return tx
