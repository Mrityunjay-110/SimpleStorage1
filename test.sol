// SPDX-License-Identifier: MIT

pragma solidity ^0.8.15;

/*contract MyContract{
    function add(uint x,uint y) external pure returns (uint){
        return x+y;
    }
}*/
contract SimpleStorage{
    uint myUint;

    struct People{
        uint256 myUint;
        string name;

    }
    People[] public  people;
    mapping(string=>uint256) public nameToNumber;
    function store(uint256 _myUint) public returns(uint256){
        myUint= _myUint;
        return _myUint;
    }
    function retrieve() public view returns(uint256){
        return myUint;
    }
    function remove(string memory _s) public{
        delete nameToNumber[_s];
    }
    function addPerson(string memory _name,uint256 _myUint)public {
        people.push(People(_myUint,_name));
        nameToNumber[_name]=_myUint;
    }
}
