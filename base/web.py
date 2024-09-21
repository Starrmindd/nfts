from web3 import Web3
import os

# Connect to the Ethereum network using Infura or another provider
infura_url = "https://mainnet.infura.io/v3/a334486f863d447c90f3e07f12f6c582"
web3 = Web3(Web3.HTTPProvider(infura_url))

# ABI (Application Binary Interface) for the ERC-721 contract
erc721_abi = [
    {
        "constant": True,
        "inputs": [{"name": "_tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "owner", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_tokenId", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Contract address for the ERC-721 (replace with your specific contract address)
contract_address = Web3.to_checksum_address('0x06012c8cf97BEaD5deAe237070F9587f8E7A266d')

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=erc721_abi)

def transfer_nft(from_address, to_address, token_id, private_key):
    try:
        # Ensure the addresses are in checksum format
        from_address = Web3.to_checksum_address(from_address)
        to_address = Web3.to_checksum_address(to_address)

        # Get the nonce (transaction count) for the sending address
        nonce = web3.eth.get_transaction_count(from_address)

        # Build the transaction
        transaction = contract.functions.transferFrom(
            from_address,
            to_address,
            token_id
        ).build_transaction({
            'nonce': nonce,
            'gas': 200000,  # Estimate or set the gas limit
            'gasPrice': web3.to_wei('50', 'gwei'),  # Adjust gas price based on network conditions
        })

        # Sign the transaction with the sender's private key
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)

        # Send the transaction to the network
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Return the transaction hash
        return tx_hash

    except Exception as e:
        raise Exception(f"Error occurred during NFT transfer: {str(e)}")

def get_nft_owner(token_id):
    """Fetch the owner of the given token ID"""
    try:
        owner = contract.functions.ownerOf(token_id).call()
        return owner
    except Exception as e:
        raise Exception(f"Error fetching owner for token {token_id}: {str(e)}")

def get_balance_of_owner(address):
    """Get the balance (number of NFTs owned) by a given wallet address"""
    try:
        address = Web3.to_checksum_address(address)
        balance = contract.functions.balanceOf(address).call()
        return balance
    except Exception as e:
        raise Exception(f"Error fetching balance for address {address}: {str(e)}")
