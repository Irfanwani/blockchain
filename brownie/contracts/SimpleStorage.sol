// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract SimpleStorage {
    uint256 public unsignedInteger;

    struct People {
        uint256 number;
        string name;
    }

    People public person = People(5, "Irfan");

    People[] public people;
    mapping(string => uint256) public nametonumber;

    function store(uint256 _fav) public {
        unsignedInteger = _fav;
    }

    function retrieve() public view returns (uint256) {
        return unsignedInteger;
    }

    function addPerson(string memory _name, uint256 _number) public {
        people.push(People(_number, _name));
        nametonumber[_name] = _number;
    }
}
