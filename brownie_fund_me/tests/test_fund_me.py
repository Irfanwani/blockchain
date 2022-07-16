from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENT, get_account
from scripts.deploy import deploy_fund_me

from brownie import accounts, network, exceptions
import pytest


def test_can_fund_and_witdraw():
    account = get_account()
    fund_me = deploy_fund_me()

    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addrtofunding(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addrtofunding(account.address) == 0


# incomplete (may be wrong also)
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip('Only for local testing')
    
    fund_me = deploy_fund_me() 
    bad_actor = accounts.add() 
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({'from': bad_actor})