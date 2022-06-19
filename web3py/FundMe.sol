// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addresstofunding;
    address[] public funders;
    address public owner;

    // constructor is called right at the time of the deployment. Here i am setting the owner to the address of the acount which we are using to make the transaction.
    constructor() {
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minUSD = 50 * 10**18;

        require(
            getConvertionRate(msg.value) >= minUSD,
            "Please send more than minUSD to complete the transaction"
        ); // require function checks for the given statement whether it is right or not. It takes the condition to be checked as the first argument and the error message as the second argument.

        addresstofunding[msg.sender] += msg.value; // msg.sender and msg.value are by default added in the request and can be accessed like this.
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface pricefeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        return pricefeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface pricefeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (, int256 answer, , , ) = pricefeed.latestRoundData(); // latestRoundData actually returns 5 vallues but we are using only one of them. That is why there are blank spaces for those other 4 values which are not getting used.
        return uint256(answer * 10000000000); // multiplied by 10000000000 just to convert it into wei
    }

    function getConvertionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 10000000000; // dividing by 10000000000 as getPrice function returns in wei
        return ethAmountInUsd;
    }

    // Modifier changes the behavior of the function on which it is applied.
    modifier onlyOwner() {
        require(msg.sender == owner);
        _; // underscore shows where the function on which the modifier is applied should be called.
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance); // 'this' refers to the contract within we are.
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addresstofunding[funder] = 0;
        }

        funders = new address[](0);
    }
}
