from brownie import accounts, Lotery
from random import randint


def deploy():
    participants = ["Irfan wani", "Inbisat", "Shahid", "Imran", 'waqar']
    account = accounts[0]

    lt = Lotery.deploy({"from": account})

    [lt.addParticipant(i) for i in participants]

    countParticipants = lt.getParticipantCount()

    winnerIndex = randint(0, countParticipants - 1)

    winner = lt.selectWinner(winnerIndex)
    print(f"And the winner is : {winner}")


def main():
    deploy()
