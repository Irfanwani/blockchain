// An NFT contract
// where the tokenURI can be one of the 3 dogs
//  Randomly selected

//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract AdvancedCollectable is ERC721URIStorage, VRFConsumerBaseV2 {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;

    constructor(
        address _vrfcoordinator,
        address _linktoken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBaseV2(_vrfcoordinator, _linktoken)
        ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectable (string memory tokenURI) public returns (bytes32) {
        
    }
}
