// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <=0.9.0;

contract Lotery {
    string[] public Participants;

    function addParticipant(string memory _name) public {
        Participants.push(_name);
    }

    function getParticipantCount() public view returns(uint256) {
        return Participants.length;
    }

    modifier checkParticipants() {
        require(
            Participants.length > 1,
            "There Must be at least two participants"
        );
        _;
    }

    function selectWinner(uint256 _winnerIndex)
        public
        view
        checkParticipants
        returns (string memory)
    {
        return Participants[_winnerIndex];
    }
}
