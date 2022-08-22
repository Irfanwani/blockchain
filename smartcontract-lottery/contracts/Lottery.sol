// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

import "@openzeppelin/contracts/access/Ownable.sol";

import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;

    address payable public recentWinner;

    uint256 public usdEntryFee;
    uint256 public randomness;

    AggregatorV3Interface internal ethUsdPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;

    uint256 public fee;

    bytes32 keyhash;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfcoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfcoordinator, _link) {
        usdEntryFee = 50 * (10**18);

        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "LOTTERY is not open yet."
        );
        require(msg.value >= getEntranceFee(), "Not enough eth.");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();

        uint256 adjustedPrice = uint256(price) * (10**10);

        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;

        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "can't start a lottery yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // Also note that this is not completely  decentralised, as we are setting an owner here who can start/stop the lottery.

        // bad ways of randomness
        // uint256(
        //     keccak256(
        //         abi.encodePacked(
        //             nonce, // nonce is predictable (aka, transaction number)
        //             msg.sender, // msg.sender is predictable
        //             block.difficulty, // can actually be maniplated by the miners
        //             block.timestamp // timestamp is predictable
        //         )
        //     )
        // ) % players.length;

        // from above comments, it is clear that a miner can maniplate the whole lottery and can always win.

        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;

        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You arent in yet"
        );

        require(_randomness > 0, "random-not-found");

        uint256 indexOfWinner = _randomness % players.length;

        recentWinner = players[indexOfWinner];

        recentWinner.transfer(address(this).balance);

        //reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
