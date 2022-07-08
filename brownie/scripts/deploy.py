from brownie import accounts, SimpleStorage


def deploy_simple_storage():
    account = accounts[
        0
    ]  # brownie spins up 10 accounts for us and we are using the first one here
    # print(account)

    # account = accounts.load("testaccount") # password encrypted account created using `brownie accounts new`
    # print(account)

    simple_storage = SimpleStorage.deploy({"from": account})

    stored_value = simple_storage.retrieve()

    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    new_val = simple_storage.retrieve()

    print(new_val)


def main():
    deploy_simple_storage()
 