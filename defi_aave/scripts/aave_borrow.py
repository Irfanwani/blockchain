from scripts.get_weth import get_weth
from .helpful_scripts import get_account
from brownie import interface, config, network
from web3 import Web3
from solcx import install_solc

amount = Web3.toWei(0.1, "ether")

install_solc('0.8.10')

def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    lending_pool = get_lending_pool()

    # Approve sending out erc20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)

    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!!!")
    borrowable_eth = get_borrowable_data(lending_pool, account)
    print("lets borrow!!")

    link_eth_price_feed = config["networks"][network.show_active()][
        "link_eth_price_feed"
    ]
    link_eth_price = get_asset_price(link_eth_price_feed)

    amount_link_to_borrow = (borrowable_eth * 100) / link_eth_price

    print(
        f"Borrowing {amount_link_to_borrow} LINK ({Web3.toWei(borrowable_eth*100, 'ether')} wei)"
    )

    link_address = config["networks"][network.show_active()]["link_token"]

    borrow_tx = lending_pool.borrow(
        link_address,
        Web3.toWei(amount_link_to_borrow, "ether"),
        2,
        0,
        account.address,
        {"from": account},
    )

    borrow_tx.wait(1)
    print("we borrowed some link")
    get_borrowable_data(lending_pool, account)

    repay_all(Web3.toWei(amount_link_to_borrow, "ether"), lending_pool, account)

    print("You just deposited , borrowed and repayed with aave, brownie and chainlink")


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["link_token"],
        account,
    )

    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["link_token"],
        amount,
        2,
        account.address,
        {"from": account},
    )

    repay_tx.wait(1)
    print("repayed")


def get_asset_price(price_feed_address):
    link_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)

    latest_price = link_eth_price_feed.latestRoundData()[1]
    converted_lp = Web3.fromWei(latest_price, "ether")
    print(f"Latest link eth price is : {converted_lp}")
    return float(converted_lp)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return float(available_borrow_eth)


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.IPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )

    lending_pool_address = lending_pool_addresses_provider.getPool()

    lending_pool = interface.IPool(lending_pool_address)
    return lending_pool
