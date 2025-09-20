from mnemonic import Mnemonic
from web3 import Account

def generate_mnemonic() -> str:
    """Generate a 12-word BIP39 mnemonic phrase"""
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)

def generate_wallet():
    """Generate mnemonic, private key, and Ethereum address"""
    # Generate mnemonic
    mnemonic_phrase = generate_mnemonic()
    
    # Enable HD wallet features
    Account.enable_unaudited_hdwallet_features()
    
    # Create account from mnemonic
    account = Account.from_mnemonic(mnemonic_phrase)
    
    return {
        'mnemonic': mnemonic_phrase,
        'private_key': account.key.hex(),
        'address': account.address
    }

def save_wallet_properties(wallet, filename="wallet.properties"):
    """Save wallet data to a properties file"""
    with open(filename, 'w') as f:
        f.write(f"PRIV_KEY={wallet['private_key']}\n")
        f.write(f"ADDRESS={wallet['address']}\n")
        f.write(f"MNEMONIC={wallet['mnemonic']}\n")
    print(f"Wallet properties saved to {filename}")

if __name__ == "__main__":
    wallet = generate_wallet()
    save_wallet_properties(wallet)
    
    print("Generated wallet:")
    print(f"PRIV_KEY={wallet['private_key']}")
    print(f"ADDRESS={wallet['address']}")
    print(f"MNEMONIC={wallet['mnemonic']}")