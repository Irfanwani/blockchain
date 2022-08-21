from .helpful_scripts import get_account, get_contract, fund_with_link
from brownie import lottery, config, network
import time

def deploy_lottery():
    account = get_account()
    ltry = lottery.deploy(
        get_contract('eth_usd_price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        config['networks'][network.show_active()]['fee'],
        config['networks'][network.show_active()]['keyhash'],
        {'from': account},
        publish_source=config['networks'][network.show_active()].get("verify", False),
    )

    print('deployed lottery!!!')
    return ltry


def start_lottery():
    account = get_account()

    ltry = lottery[-1]
    starting_txn = ltry.startLottery({'from': account})
    starting_txn.wait(1)
    print('Lottery started!!!')

def enter_lottery():
    account = get_account()
    ltry = lottery[-1]
    value = ltry.getEntranceFee() + 100000000
    tx = ltry.enter({'from': account, 'value': value})
    tx.wait(1)

    print('You entered the lottery')

def end_lottery():
    account = get_account()
    ltry = lottery[-1]

    tx = fund_with_link(ltry.address)
    tx.wait(1)
    print('here is tx: \n',tx)
    ending_txn = ltry.endLottery({'from': account})
    print('ending txn done')
    ending_txn.wait(1)
    time.sleep(60)
    print(f'{ltry.recentWinner()} is the new winner')
    print('Lottery ended!!!')

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()