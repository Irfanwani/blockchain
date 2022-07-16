// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address public owner;

    mapping(address => uint256) public addrtofunding;
    address[] public donors;
    AggregatorV3Interface public priceFeed;
    
    constructor(address _pricefeed) public {
        priceFeed = AggregatorV3Interface(_pricefeed);
        owner = msg.sender;
    }

    function fund() public payable {
        addrtofunding[msg.sender] += msg.value;
        donors.push(msg.sender);
    }

    function getPrice() public view returns (uint256) {
        (, int256 latestPrice, , , ) = priceFeed.latestRoundData();

        return uint256(latestPrice * 10000000000);
    }

    function convertToUsd(uint256 ethamount) public view returns (uint256) {
        uint256 rate = getPrice();

        uint256 result = (rate * ethamount) / 10000000000;

        return result;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minUSD = 50 * 10 ** 18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10 ** 18;
        return (minUSD * precision) / price;
    }

    modifier usercheck() {
        require(msg.sender == owner, "You cannot perform this action");
        _;
    }

    function withdraw() public payable usercheck {
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 i = 0; i < donors.length; i++) {
            addrtofunding[donors[i]] = 0;
        }

        donors = new address[](0);
    }
}
