from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()
    # pass the pricefeed address to the fundme contract (or more generally, all the constructor parameters are passed in this deploy method)

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"the active network is {network.show_active()}\nDeploying Mocks...")

        mock_aggreagtor = MockV3Aggregator.deploy(18, 2000000000000000000000, {"from": account})

        price_feed_address = mock_aggreagtor.address
        print("Mocks deployed!")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config['networks'][network.show_active()].get('verify'),
    )

    print(f"contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
