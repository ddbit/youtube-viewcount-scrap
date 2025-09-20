import json
from web3 import Web3
from eth_account import Account
import argparse
import sys

def load_properties(filename):
    """Load properties from a file"""
    properties = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    properties[key] = value
        return properties
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        sys.exit(1)

def load_abi(filename):
    """Load contract ABI from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        sys.exit(1)

class ContractPerformance:
    def __init__(self):
        self.contract_props = load_properties('contract.properties')
        self.wallet_props = load_properties('wallet.properties')
        self.abi = load_abi('contract.abi')
        
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(self.wallet_props['RPC_URL']))
        
        if not self.w3.is_connected():
            print("Error: Could not connect to Ethereum node")
            sys.exit(1)
        
        # Load account from private key
        self.account = Account.from_key(self.wallet_props['PRIV_KEY'])
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=self.contract_props['CONTRACT_ADDRESS'],
            abi=self.abi
        )
        
        print(f"Connected to {self.contract_props['CHAIN_NAME']} network")
        print(f"Using account: {self.account.address}")
        print(f"Contract address: {self.contract_props['CONTRACT_ADDRESS']}")

    def set_indicator(self, key_hex, indicator_value):
        """Call the set function on the contract"""
        try:
            # Convert hex string to bytes32
            key_bytes = Web3.to_bytes(hexstr=key_hex)
            
            # Build transaction
            transaction = self.contract.functions.set(key_bytes, indicator_value).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 50000,
                'gasPrice': self.w3.to_wei('1', 'gwei'),
                'chainId': int(self.contract_props['CHAIN_ID'], 16)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.wallet_props['PRIV_KEY'])
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"Set transaction sent: {tx_hash.hex()}")
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction confirmed in block: {receipt.blockNumber}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error calling set function: {e}")
            return None

    def set_owner(self, new_owner_address):
        """Call the setOwner function on the contract"""
        try:
            # Validate address
            if not Web3.is_address(new_owner_address):
                print(f"Error: {new_owner_address} is not a valid Ethereum address")
                return None
            
            # Build transaction
            transaction = self.contract.functions.setOwner(new_owner_address).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 50000,
                'gasPrice': self.w3.to_wei('1', 'gwei'),
                'chainId': int(self.contract_props['CHAIN_ID'], 16)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.wallet_props['PRIV_KEY'])
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"SetOwner transaction sent: {tx_hash.hex()}")
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction confirmed in block: {receipt.blockNumber}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error calling setOwner function: {e}")
            return None

    def get_owner(self):
        """Get current owner of the contract"""
        try:
            owner = self.contract.functions.owner().call()
            print(f"Current owner: {owner}")
            return owner
        except Exception as e:
            print(f"Error getting owner: {e}")
            return None

    def get_indicator(self, key_hex):
        """Get indicator value for a given key"""
        try:
            key_bytes = Web3.to_bytes(hexstr=key_hex)
            indicator = self.contract.functions.Indicator(key_bytes).call()
            print(f"Indicator for key {key_hex}: {indicator}")
            return indicator
        except Exception as e:
            print(f"Error getting indicator: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Interact with Performance contract')
    parser.add_argument('action', choices=['set', 'setOwner', 'getOwner', 'getIndicator'], 
                        help='Action to perform')
    parser.add_argument('--key', type=str, help='Key for set/getIndicator (hex string)')
    parser.add_argument('--value', type=int, help='Value for set function')
    parser.add_argument('--address', type=str, help='Address for setOwner function')
    
    args = parser.parse_args()
    
    perf = ContractPerformance()
    
    if args.action == 'set':
        if not args.key or args.value is None:
            print("Error: --key and --value are required for set action")
            sys.exit(1)
        perf.set_indicator(args.key, args.value)
    
    elif args.action == 'setOwner':
        if not args.address:
            print("Error: --address is required for setOwner action")
            sys.exit(1)
        perf.set_owner(args.address)
    
    elif args.action == 'getOwner':
        perf.get_owner()
    
    elif args.action == 'getIndicator':
        if not args.key:
            print("Error: --key is required for getIndicator action")
            sys.exit(1)
        perf.get_indicator(args.key)

if __name__ == "__main__":
    main()