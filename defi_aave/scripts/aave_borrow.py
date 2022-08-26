from scripts.get_weth import get_weth
from .helpful_scripts import get_account
from brownie import interface, config, network
from web3 import Web3

amount = Web3.toWei(0.005, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    lending_pool = get_lending_pool()
    print(lending_pool)

    # Approve sending out erc20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)

    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!!!")
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("lets borrow!!")

    dai_eth_price_feed = config["networks"][network.show_active()]["dai_eth_price_feed"]
    dai_eth_price = get_asset_price(dai_eth_price_feed)

    amount_dai_to_borrow = (borrowable_eth * 0.75) / dai_eth_price

    print(
        f"Borrowing {amount_dai_to_borrow} DAI ({Web3.toWei(borrowable_eth*0.75, 'ether')} wei)"
    )

    dai_address = config["networks"][network.show_active()]["dai_token"]

    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(borrowable_eth * 0.75, "ether"),
        1,
        0,
        account.address,
        {"from": account, 'gasPrice': 9000000},
    )

    borrow_tx.wait(1)
    print("we borrowed some DAI")
    get_borrowable_data(lending_pool, account)

    # repay_all(amount, lending_pool, account)

    print("You just deposited , borrowed and repayed with aave, brownie and chainlink")


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )

    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )

    repay_tx.wait(1)
    print("repayed")


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)

    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_lp = Web3.fromWei(latest_price, "ether")
    print(f"Latest Dai eth price is : {converted_lp}")
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

    print(f"You have {total_collateral_eth} worth of eth deposited")
    print(f"You have {total_debt_eth} worth of eth borrowed")
    print(f"You can borrow {available_borrow_eth} worth of eth")
    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )

    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
