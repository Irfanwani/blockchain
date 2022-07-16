from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENT

def deploy_fund_me():
    account = get_account()
    # pass the pricefeed address to the fundme contract (or more generally, all the constructor parameters are passed in this deploy method)

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks (which are locally downloaded sol file/s which immitate some interface locally)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config['networks'][network.show_active()].get('verify'),
    )

    print(f"contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
