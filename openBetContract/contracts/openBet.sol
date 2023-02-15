// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;


contract openBet {
    address payable custodialWallet;
    address payable payableOwner;
    address owner;
    address payable player1;
    address payable player2;
    uint256 player1Bet;
    uint256 player2Bet;
    uint256 totalBet;
    bool player1Won;
    bool player2Won;
    uint256 fee = 5; // 5%

    constructor() {
        owner = payable (msg.sender);
    }


    function setPlayers(address payable _player1, address payable _player2) public {
        require(msg.sender == owner, "Only the owner can set the players.");
        player1 = _player1;
        player2 = _player2;
    }



    struct Bet {
    string name;
    address payable player1;
    address payable player2;
    uint256 player1Bet;
    uint256 player2Bet;
    uint totalBetAmount;
    address payable _winner;
    }
    
    Bet[] public bets;
    uint public totalBetMoney = 0;

    mapping (address => uint) public numBetsAddress;

    function getTotalBetAmount (uint _winner) public view returns (uint) {
        return bets[_winner].totalBetAmount;
        }

    function createBet (address payable _player) external payable {       
        require (msg.sender != owner, "owner can't make a bet");
        require (numBetsAddress[msg.sender] == 0, "you have already placed a bet");
        require (msg.value > 0.01 ether, "bet more");

       //bets.push(Bet(_winner, player1Bet, player2Bet, owner));

        if (player1 == _player) {
        player1Bet += msg.value;
        } else if (player2 == _player) {
            player2Bet += msg.value;
        } else {
            custodialWallet.transfer(msg.value);
        }
    }

    //function deposit(address payable _player) public payable {
    //    require(msg.value > 1 , "Deposit must be greater than 0 ether");
    //    if (_player1 == player1) {
    //        player1Bet += msg.value;
    //    } else if (_player1 == player2) {
    //        player2Bet += msg.value;
    //    } else {
    //        custodialWallet.transfer(msg.value);
    //    }
    //}

   

    function setResult(bool _player1Won, bool _player2Won) public {
        require(msg.sender == owner, "Only the owner can set the result.");
        require(_player1Won != _player2Won, "Both players cannot win.");
        player1Won = _player1Won;
        player2Won = _player2Won;

        if (player1Won) {
            player1.transfer(player2Bet);
            uint256 feeAmount = player2Bet * fee / 100;
            custodialWallet.transfer(feeAmount);
            payableOwner.transfer(player2Bet - feeAmount);
        } else {
            player2.transfer(player1Bet);
            uint256 feeAmount = player1Bet * fee / 100;
            custodialWallet.transfer(feeAmount);
            payableOwner.transfer(player1Bet - feeAmount);
        }
    }
}