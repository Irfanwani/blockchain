from brownie import lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery

def test_get_entrance_fee():
    ltry = deploy_lottery()
    entrance_fee = ltry.getEntranceFee()
    
     


