# Practical 17 – Business Network using Hyperledger (Composer)

**Aim:** Write a program to create a Business Network using Hyperledger.

Following the manual, this uses **Hyperledger Composer** to build a **"hardware-assets"** network. An organisation records its hardware (laptops etc.) as **assets** owned by **employees (participants)**, and every **Allocate transaction** that hands a device to a new employee is recorded on the blockchain.

## Files
```
Practical_17_Hyperledger_Business_Network/
├── hardware-assets/                  ← the business network source
│   ├── package.json                  ← network name/version (needed by Composer)
│   ├── models/org.lp3.hardware.cto   ← MODEL file: participant, asset, transaction, event
│   ├── lib/logic.js                  ← SCRIPT file: transaction processor function
│   ├── permissions.acl               ← ACCESS CONTROL rules
│   └── README.md
├── hardware-assets.bna               ← ready-made Business Network Archive (zip of the folder above)
└── test-data/                        ← JSON to paste in the "Test" tab, in this order
    ├── 1_employee_01.json
    ├── 2_employee_02.json
    ├── 3_hardware_MAC01.json
    └── 4_transaction_allocate.json
```

## Important note before you start
Hyperledger Composer was **deprecated in 2019**, and the **online** Playground mentioned in the manual (`composer-playground.mybluemix.net`) **no longer works**. You need to run Playground **locally**. The two options below both work on Windows, Linux and macOS. Option A is the easiest.

### Option A: Composer Playground in Docker (recommended)
1. Install **Docker Desktop** (Windows/macOS) or Docker Engine (Linux) from https://docs.docker.com/get-docker/ and start it.
2. Run:
   ```bash
   docker run --name composer-playground --publish 8080:8080 hyperledger/composer-playground
   ```
   The next time, just run `docker start composer-playground`.
3. Open **http://localhost:8080** in your browser and click **Let's Blockchain!**

### Option B: Composer Playground with Node.js 8
Composer only works with **old Node.js (v8.x)**, so use a Node version manager to keep it separate from your normal Node.
1. Install a version manager:
   - Linux/macOS: **nvm**, from https://github.com/nvm-sh/nvm (follow its install line)
   - Windows: **nvm-windows**, from https://github.com/coreybutler/nvm-windows/releases (run `nvm-setup.exe`)
2. Run:
   ```bash
   nvm install 8
   nvm use 8
   npm install -g composer-cli@0.20 composer-playground@0.20
   composer-playground
   ```
3. A browser opens at **http://localhost:8080**.

## Running the practical in Playground
Playground's **Web Browser** connection simulates the blockchain inside the browser, so you don't need a full Fabric network.

**Deploy the network.** You can do this either way:
- **Quick:** click **Deploy a new business network**. Under *Based on an existing network...*, click **Drop here to upload or browse** and select `hardware-assets.bna`. Give it a name and click **Deploy**.
- **Manually, as the manual shows:** click **Deploy a new business network** → choose **empty-business-network** → name it `hardware-assets` → **Deploy**. Then **Connect now**. In the **Define** tab:
  1. **Add a file → Model File (.cto)**, and paste in `models/org.lp3.hardware.cto` (replace the sample content)
  2. **Add a file → Script File (.js)**, and paste in `lib/logic.js`
  3. Open **Access Control (permissions.acl)** and paste in `permissions.acl`
  4. Click **Deploy changes** at the bottom left.

**Test it** (click the **Test** tab at the top):
1. **Employee → + Create New Participant.** Paste `test-data/1_employee_01.json` → **Create New**. Do the same with `2_employee_02.json`.
2. **Hardware → + Create New Asset.** Paste `test-data/3_hardware_MAC01.json` → **Create New**. The owner is Employee 01.
3. **Submit Transaction** (left panel). Transaction Type is **Allocate**. Paste `test-data/4_transaction_allocate.json` → **Submit**.
4. Open **Hardware** again. MAC01's owner is now **Employee#02**.
5. Open **All Transactions** to see every recorded transaction with its ID and timestamp: adding the participants, adding the asset, and Allocate. Click **view record** for details, including the emitted `HardwareAllocated` event.
6. **Bonus check:** submit the same Allocate transaction again. It's **rejected** with *"Hardware MAC01 is already allocated to employee 02"*, which shows the validation in `logic.js`.

## Input guide (what to enter in Playground)
All input is **JSON**, pasted into Playground's *Test* tab. The ready-made files are in `test-data/`. Enter them **in order**, because the hardware refers to Employee 01, so the employee must exist first.

| Step | Where | Paste this file | Key fields you may change |
|---|---|---|---|
| 1 | Employee → Create New Participant | `1_employee_01.json` | `employeeId` (must be unique), `firstName`, `lastName`, `department` (optional) |
| 2 | Employee → Create New Participant | `2_employee_02.json` | same |
| 3 | Hardware → Create New Asset | `3_hardware_MAC01.json` | `hardwareId` (unique), `name`, `type`, `description`, `quantity` (a number), `owner` = `resource:org.lp3.hardware.Employee#<employeeId>` |
| 4 | Submit Transaction → type **Allocate** | `4_transaction_allocate.json` | `hardware` = `resource:org.lp3.hardware.Hardware#<hardwareId>`, `newOwner` = `resource:org.lp3.hardware.Employee#<employeeId>` |

Rules:
- `"$class"` must be the full type name, e.g. `org.lp3.hardware.Employee`.
- Relationships are written as `resource:<namespace>.<Type>#<id>`.
- `quantity` is a Double, so write `1` or `1.0`, **without** quotes.
- Allocating to the employee who already owns the hardware is rejected (validation in `logic.js`).

### (Optional) Deploying on a real Hyperledger Fabric network
This is the manual's steps 13–14. It needs Linux/macOS (or WSL2) with Docker and Node 8, plus the Fabric dev servers from the Composer tutorial ("fabric-dev-servers"). Then, from the folder that contains `hardware-assets/`:
```bash
composer archive create -t dir -n hardware-assets          # creates hardware-assets@0.0.1.bna
composer network install -c PeerAdmin@hlfv1 -a hardware-assets@0.0.1.bna
composer network start -n hardware-assets -V 0.0.1 -c PeerAdmin@hlfv1 -A admin -S adminpw -f networkadmin.card
composer card import -f networkadmin.card
composer network ping -c admin@hardware-assets
composer-rest-server                                       # optional: REST API on http://localhost:3000
```
For the practical exam, the Playground (Option A or B) is enough.

## Concepts
- **Hyperledger:** an open-source umbrella project by the **Linux Foundation** for **enterprise / permissioned blockchains**. Only known, authorised members can join. Compare this with public blockchains like Bitcoin and Ethereum, where anyone can join.
- **Hyperledger Fabric:** a modular permissioned blockchain framework. Its components include peers, an ordering service, channels and chaincode (smart contracts). There's no cryptocurrency and no mining.
- **Hyperledger Composer:** a development toolset on top of Fabric for quickly modelling a **business network**. You describe the network in a model file, write logic in JavaScript and set permissions with an ACL, and Composer packages it into a **.bna (Business Network Archive)**.
- **Business network building blocks:**
  - **Participant:** a member of the network (`Employee`)
  - **Asset:** a tangible or intangible item of value that is owned and exchanged (`Hardware`)
  - **Transaction:** an operation that changes the state of assets (`Allocate`)
  - **Event:** a notification emitted by a transaction that applications can listen to (`HardwareAllocated`)
  - **Registry:** the stored collection of all assets or participants of a type, i.e. the world state
- **CTO modelling language:** `namespace` groups the types. `identified by` sets the unique ID field. `o` declares a normal property, and `-->` declares a **relationship** (a reference to another resource, like a foreign key). `optional` marks a field that isn't required.
- **Transaction processor function (logic.js):** the JavaScript that runs when the transaction is submitted. The `@param {namespace.Type}` and `@transaction` annotations tell Composer which transaction it handles. If it throws an error, the whole transaction is **rolled back**.
- **Access Control Language (ACL):** rules that say which *participant* can perform which *operation* (CREATE / READ / UPDATE / DELETE / ALL) on which *resource*, and whether to ALLOW or DENY it.
- **Immutability and traceability:** every create and allocate action is a transaction stored on the ledger and can't be altered. That gives a full audit trail of who owned the hardware and when.

## Code walkthrough
- **`org.lp3.hardware.cto`**
  - `participant Employee`: employeeId (key), first/last name, and an optional department
  - `asset Hardware`: hardwareId (key), name, type, description, quantity, and `--> Employee owner` (relationship)
  - `transaction Allocate`: refers to the hardware being moved and the new owner
  - `event HardwareAllocated`: records the old and new owner IDs
- **`logic.js`: `allocateHardware(allocate)`**
  1. reads the old and new owner IDs with `getIdentifier()`
  2. throws an error if it's the same owner, which rejects the transaction and rolls it back
  3. sets `hardware.owner = allocate.newOwner`
  4. `getAssetRegistry('org.lp3.hardware.Hardware')` → `update(hardware)` saves the change to the world state
  5. creates the event with `getFactory().newEvent(...)` and calls `emit(event)`
- **`permissions.acl`**: `AllAccess` gives every participant full access to our namespace (fine for a demo). `SystemACL` and `NetworkAdminUser` give the system and admin the access they need.
- **`package.json`**: the network name and version. `"engines": {"composer": "^0.20.0"}` is required by Composer 0.20.

> The manual uses the namespace `com.kpbird` from the original tutorial. This code uses `org.lp3.hardware` and the same structure: Hardware asset, Employee participant, Allocate transaction. If you change the namespace, change it in all four files and in the test JSON.
