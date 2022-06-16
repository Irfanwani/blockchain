pragma solidity >= 0.7.0 <0.9.0;

contract SimpleStorage {
    uint256 unsignedInteger; // uint is used to declare an absolute number

    function store(uint _fav) public {
        unsignedInteger = _fav;
    }
    
}



// int256 anyInteger = -5;
//     bool boolean = false;
//     address myWalletAddress = 0x954dC1202b3997e2785fCDfEcFfb52b5D591a26d; //used to store any address of some account 
//     bytes32 someval = "cat";