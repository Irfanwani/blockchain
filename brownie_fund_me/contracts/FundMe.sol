// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address owner;

    mapping(address => uint256) public addrtofunding;
    address[] public donors;

    constructor() {
        owner = msg.sender;
    }

    function fund() public payable {
        addrtomapping[msg.sender] += msg.value;
        donors.push(msg.sender);
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface result = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (, int256 latestPrice, , , ) = result.latestRoundData();

        return uint256(latestPrice * 10000000000);
    }

    function convertToUsd(uint256 ethamount) public view returns (uint256) {
        uint256 rate = getPrice();

        uint256 result = (rate * ethamount) / 10000000000;

        return result;
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
