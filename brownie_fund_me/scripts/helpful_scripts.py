from brownie import accounts, network, config, MockV3Aggregator

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        print('Development env:::')
        return accounts[0]

    else:
        print('Deployment Env:::')
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}\nDeploying mocks...")

    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})

    print("Mock deployed!!!")
