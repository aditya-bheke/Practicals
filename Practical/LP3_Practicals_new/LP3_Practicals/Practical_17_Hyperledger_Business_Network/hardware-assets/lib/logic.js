/**
 * Practical 17 : Business Network using Hyperledger Composer
 * Script file (logic.js) - transaction processor functions (the "chaincode" logic).
 *
 * The comment annotations are REQUIRED by Composer:
 *   @param {namespace.TransactionType} name  -> which transaction this function handles
 *   @transaction                             -> marks it as a transaction processor
 */

'use strict';

/**
 * Allocate a hardware asset to a new employee.
 * @param {org.lp3.hardware.Allocate} allocate - the Allocate transaction instance
 * @transaction
 */
async function allocateHardware(allocate) {
    const hardware = allocate.hardware;
    const oldOwnerId = hardware.owner.getIdentifier();
    const newOwnerId = allocate.newOwner.getIdentifier();

    // validation - rejecting the transaction rolls back every change
    if (oldOwnerId === newOwnerId) {
        throw new Error('Hardware ' + hardware.hardwareId + ' is already allocated to employee ' + newOwnerId);
    }

    // 1. change the owner of the asset
    hardware.owner = allocate.newOwner;

    // 2. save the updated asset in the asset registry (world state)
    const assetRegistry = await getAssetRegistry('org.lp3.hardware.Hardware');
    await assetRegistry.update(hardware);

    // 3. emit an event so applications can be notified
    const event = getFactory().newEvent('org.lp3.hardware', 'HardwareAllocated');
    event.hardware = hardware;
    event.oldOwnerId = oldOwnerId;
    event.newOwnerId = newOwnerId;
    emit(event);
}
