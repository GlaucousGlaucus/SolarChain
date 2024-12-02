from algosdk import account, mnemonic
from algosdk.transaction import SuggestedParams, PaymentTxn, SignedTransaction, AssetConfigTxn
from algosdk.v2client import algod
from algosdk.v2client.algod import AlgodClient
from algosdk import transaction

from playground.account_constants import ACCOUNTS, Account

# LocalNet configuration
TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # Default AlgoKit LocalNet token
SERVER_ADDRESS = "http://localhost:4001"  # Default AlgoKit LocalNet endpoint

# Initialize the Algod client
algod_client: AlgodClient = AlgodClient(TOKEN, SERVER_ADDRESS)
print("Algod Client Created")

# Check the connection by fetching the node status
try:
    status = algod_client.status()
    print("Connected to Algorand Network.")
    print("Network Status:", status)
except Exception as e:
    print("Failed to connect:", e)

# Generate address and mnemonic if needed
acc1 = Account(ACCOUNTS[0])
acc2 = Account(ACCOUNTS[1])

print("Public Address:", acc1.address)
print("My address:", acc1.private_key)
print("My mnemonic:", acc1.mnemonic)

# amount = 1 * 1000000  # Amount in microAlgos (0.1 ALGO)

params: SuggestedParams = algod_client.suggested_params()

def create_asset():
    # Create the transaction
    txn = transaction.AssetConfigTxn(
        sender=acc1.address,
        sp=params,
        default_frozen=False,
        unit_name="units",
        asset_name="Electrical Units",
        manager=acc1.address,
        reserve=acc1.address,
        freeze=acc1.address,
        clawback=acc1.address,
        url="https://path/to/my/asset/details",
        total=1000,
        decimals=0,
    )

    # Sign the transaction with the private key
    signed_txn: SignedTransaction = txn.sign(acc1.private_key)

    # Send the transaction
    tx_id: str = algod_client.send_transaction(signed_txn)
    print(f"Sent asset create transaction with txid: {tx_id}")
    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    # grab the asset id for the asset we just created
    created_asset = results["asset-index"]
    print(f"Asset ID created: {created_asset}")

created_asset = 1016

def receive_asset():
    optin_txn = transaction.AssetOptInTxn(
        sender=acc2.address, sp=params, index=created_asset
    )
    signed_optin_txn = optin_txn.sign(acc2.private_key)
    txid = algod_client.send_transaction(signed_optin_txn)
    print(f"Sent opt in transaction with txid: {txid}")

    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

def transfer_asset():
    # Create transfer transaction
    xfer_txn = transaction.AssetTransferTxn(
        sender=acc1.address,
        sp=params,
        receiver=acc2.address,
        amt=1,
        index=created_asset,
    )
    signed_xfer_txn = xfer_txn.sign(acc1.private_key)
    txid = algod_client.send_transaction(signed_xfer_txn)
    print(f"Sent transfer transaction with txid: {txid}")

    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

transfer_asset()