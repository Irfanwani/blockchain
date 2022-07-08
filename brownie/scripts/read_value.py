from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[
        -1
    ]  # SimpleStorage returns an array of deployments made for SimpleStorage contract. So we can access it like a list in python. Here i used -1 as index to get the latest deployment.

    # To work with a contract, we always need to know two things;
    # ABI of contract
    # Address
    val = simple_storage.retireve()
    print(val)


def main():
    read_contract()
