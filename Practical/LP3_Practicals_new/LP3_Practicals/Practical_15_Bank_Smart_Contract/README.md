# Practical 15 – Bank Account Smart Contract (Solidity)

**Aim:** Write a smart contract on a test network for a customer's bank account, with these operations: **Deposit money, Withdraw money, Show balance.**

## Files
| File | Purpose |
|---|---|
| `Bank.sol` | The smart contract (Solidity 0.8.x) |

## Setup: nothing to install
Everything runs in the browser using the **Remix IDE**. It works on any OS with Chrome, Firefox, Edge or Brave.

### Option A: Remix VM (quickest, recommended for the practical exam)
Remix gives you 10 test accounts with 100 fake ETH each. No MetaMask is needed.
1. Open **https://remix.ethereum.org**.
2. In the **File Explorer** (left panel), click **Create new file**, name it `Bank.sol`, and paste in the code from `Bank.sol`. You can also use **Upload files** to upload it.
3. Open the **Solidity Compiler** tab (2nd icon). Choose any compiler version **0.8.x** (for example 0.8.26) and click **Compile Bank.sol**. A green tick means success.
4. Open the **Deploy & Run Transactions** tab (3rd icon).
   - Environment: **Remix VM (Cancun)** or any "Remix VM".
   - Contract: **Bank**, then click **Deploy**.
5. Expand the deployed contract under **Deployed Contracts** and test it:
   - **Deposit:** at the top of the panel, set **Value** to e.g. `2` and change the unit from *Wei* to **Ether**. Then click the red **deposit** button. Your account's ETH drops by 2 (plus a little gas).
   - **Show balance:** click **getBalance**. It shows `2000000000000000000` (2 ETH in wei).
   - **Withdraw:** type `1000000000000000000` (1 ETH in wei) next to **withdraw** and click it. Then click **getBalance** again and it shows 1 ETH.
   - **Insufficient balance:** try withdrawing more than you have. The transaction **reverts** with *"Insufficient balance"* in the terminal.
   - **Separate balances:** switch to another account in the *Account* dropdown and click **getBalance**. It shows 0, because each customer has their own balance.
6. Click any transaction in the Remix terminal at the bottom to see its hash, gas used and the emitted `Deposited`/`Withdrawn` events.

### Option B: a real test network with MetaMask (Sepolia)
1. Install MetaMask (see Practicals 13/14) and switch to the **Sepolia** test network. Turn on *Show test networks* in settings if it's hidden.
2. Get free test ETH from a Sepolia faucet. For example, search "Sepolia faucet" and use Google Cloud's or Alchemy's faucet.
3. In Remix **Deploy & Run**, choose Environment **Injected Provider – MetaMask** and approve the connection.
4. Click **Deploy** and confirm in MetaMask. Then use deposit/withdraw/getBalance as above. Every state-changing call opens a MetaMask confirmation that shows the gas fee.
5. The contract address and every transaction can be viewed on **https://sepolia.etherscan.io**.

> Tip for converting units: 1 Ether = 10¹⁸ wei. You can also use https://eth-converter.com.

## Input guide (what to enter in Remix)
| Function | Where to type the input | Example |
|---|---|---|
| **deploy** | nothing (no constructor arguments) | click **Deploy** |
| **deposit** | the **VALUE** box at the top of *Deploy & Run* (next to the unit dropdown). The deposit button itself has no input box. | VALUE = `2`, unit = **Ether** → click **deposit** |
| **withdraw** | the box next to the **withdraw** button. The amount is in **wei**. | `1000000000000000000` (= 1 ETH) → click **withdraw** |
| **getBalance** | none | click → shows your balance in wei |
| **getBankBalance** | none | click → total ETH held by the contract |
| **owner** | none | click → address of the deployer |

Wei conversions: 1 ETH = `1000000000000000000` (1 followed by 18 zeros), 0.5 ETH = `500000000000000000`, 0.1 ETH = `100000000000000000`.

**Demo sequence for the examiner:**
1. Deposit **5 Ether** (VALUE 5, unit Ether) → getBalance = `5000000000000000000`
2. Withdraw `2000000000000000000` → getBalance = `3000000000000000000`
3. Withdraw `9000000000000000000` → reverts with **"Insufficient balance"**
4. Set VALUE back to 0 and click deposit → reverts with **"Deposit amount must be greater than 0"**
5. Switch to a different *Account* → getBalance = `0`, because each customer has their own balance
6. **Remember** to reset VALUE to 0 before calling withdraw. Otherwise Remix tries to send Ether to a non-payable function, and the call fails.

## Concepts
- **Smart contract:** a program stored on the blockchain that runs automatically when called. Once deployed it can't be changed, and every execution is recorded in a transaction.
- **Solidity:** a statically typed language for Ethereum smart contracts. `pragma solidity ^0.8.0;` means "any compiler from 0.8.0 up to (but not including) 0.9.0". Version 0.8 also has **built-in overflow checks**.
- **Ethereum account / address:** `msg.sender` is the address that called the function, i.e. the current customer.
- **mapping(address => uint256):** a key-value store, like a dictionary, from each customer's address to their balance. Missing keys default to 0.
- **payable:** a function marked `payable` can receive Ether. The amount sent is `msg.value`, in **wei**.
- **require(condition, "message"):** validates input. If the condition is false, the transaction **reverts**, which undoes all state changes, and the message is returned.
- **view:** the function only reads data, so calling it from outside costs no gas.
- **Gas:** the fee paid (in ETH) for every operation that changes blockchain state. Deposit and withdraw cost gas. getBalance doesn't.
- **Events (`emit`):** logs stored on the blockchain that front-ends and Etherscan can read.
- **Checks-Effects-Interactions pattern:** in `withdraw`, the balance is reduced **before** sending Ether. This prevents **re-entrancy attacks**, the bug behind the famous DAO hack. `call{value: amount}("")` is the currently recommended way to send Ether.
- **Test network (Sepolia):** a copy of Ethereum that uses free test ETH, for safe development.

## Code walkthrough
| Part | Explanation |
|---|---|
| `mapping(address => uint256) private balances` | Stores each customer's balance |
| `address public owner` + `constructor()` | Records who deployed the contract. It runs once, at deployment. |
| `event Deposited / Withdrawn` | Logs for each transaction |
| `deposit()` | `payable`. Checks `msg.value > 0`, adds it to the caller's balance and emits `Deposited`. |
| `withdraw(amount)` | Checks amount > 0 and that the balance is enough, reduces the balance, sends the Ether back with `call`, checks it was sent and emits `Withdrawn` |
| `getBalance()` | Returns the caller's own balance (view) |
| `getBankBalance()` | Total Ether held by the contract for all customers |

> The manual's sample code uses the old `pragma solidity ^0.4.19`, where `msg.sender.transfer()` worked directly. Current Remix compilers are 0.8.x, so this version uses the modern syntax: `constructor()`, `payable(msg.sender)`, `call{value: ...}`. The logic is the same as the manual's `Bank` contract.
