// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/*
 * Practical 15 : Smart contract for a customer's Bank account
 * Operations   : Deposit money, Withdraw money, Show balance
 * Run it in    : Remix IDE (https://remix.ethereum.org), on the "Remix VM" or on a
 *                test network such as Sepolia through MetaMask ("Injected Provider").
 *
 * Every customer (Ethereum address) has their own balance inside this contract.
 * Real Ether is sent with deposit() and returned with withdraw().
 */
contract Bank {
    // balance of every customer, indexed by their account address
    mapping(address => uint256) private balances;

    // the account that deployed the contract (the "bank manager")
    address public owner;

    // events are written to the blockchain log -> visible in Remix / Etherscan
    event Deposited(address indexed customer, uint256 amount);
    event Withdrawn(address indexed customer, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    // ---------------- Deposit money ----------------
    // 'payable' lets the function receive Ether. The amount sent is msg.value (in wei).
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    // ---------------- Withdraw money ----------------
    // amount is in wei (1 ether = 10^18 wei)
    function withdraw(uint256 amount) public {
        require(amount > 0, "Withdraw amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        // update the state BEFORE sending Ether (Checks-Effects-Interactions,
        // protects against re-entrancy attacks)
        balances[msg.sender] -= amount;

        (bool sent, ) = payable(msg.sender).call{value: amount}("");
        require(sent, "Ether transfer failed");

        emit Withdrawn(msg.sender, amount);
    }

    // ---------------- Show balance ----------------
    // 'view' = only reads data, so calling it costs no gas
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }

    // total Ether held by the contract for all customers
    function getBankBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
