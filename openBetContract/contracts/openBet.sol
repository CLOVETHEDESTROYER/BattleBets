// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/security/Pausable.sol";
//import "@openzeppelin/contracts/access/Ownable.sol";
import "@thirdweb-dev/contracts/extension/Ownable.sol";
import "@thirdweb-dev/contracts/extension/Permissions.sol";

contract openBet is Ownable, Permissions, Pausable {
    address payable custodialWallet;
    address payable payableOwner;
    address payable public owner;
    address payable public player1;
    address payable public player2;
    uint256 public player1Bet;
    uint256 public player2Bet;
    uint256 playerBet;
    uint public pot;
    uint public ownerFee;
    mapping(address => uint) public playerBalances;
    bool player1Won;
    bool player2Won;
    uint256 fee = 5; // 5%

    constructor() {
        owner = payable (msg.sender);
        pot = 0;
    }

    //ownable function.  Change this to your wallet. 
    function _canSetOwner() internal virtual view override returns (bool) {
        return msg.sender == 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
    }


    function setPlayers(address payable _player1, address payable _player2) public {
        //only 2 players at a time
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
    //uint public totalBetMoney += msg.value;

    mapping (address => uint) public numBetsAddress;

    function getTotalBetAmount (uint _winner) public view returns (uint) {
        return bets[_winner].totalBetAmount;
        }

    function placeBet (address payable _player) external payable {       
        require (msg.sender != owner, "owner can't make a bet");
        require (numBetsAddress[msg.sender] == 0, "you have already placed a bet");
        require (msg.value > 0.01 ether, "bet more");

       //bets.push(Bet(_winner, player1Bet, player2Bet, owner));

        if (player1 == _player) {
        player1Bet += msg.value;
        } else if (player2 == _player) {
            player2Bet += msg.value;
        } else {
            payableOwner.transfer(msg.value);
        }
        pot += msg.value;
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

   

    function setResult(bool _player1Won, bool _player2Won) payable public {
        require(msg.sender == owner, "Only the owner can set the result.");
        require(_player1Won != _player2Won, "Both players cannot win.");
        player1Won = _player1Won;
        player2Won = _player2Won;

        if (player1Won) 
            ownerFee = pot / 20;
            uint payout = pot - ownerFee;
            player1.transfer(payout);
            owner.transfer(ownerFee);
           
         if (player2Won) {
            ownerFee = pot / 20;
            payout = pot - ownerFee;
            player2.transfer(payout);
            owner.transfer(ownerFee);
        }
    }

    function playAgain() public {
        //require(msg.sender == owner, "Only the owner can reset the contract.");
        pot = 0;
        ownerFee = 0;
        player1Bet = 0;
        player2Bet = 0;
    }
}
