# youtube-viewcount-scrap

## Ethereum Wallet Generator

### Prerequisites

Install required Python packages:

```bash
pip install web3 mnemonic
```

### Usage

Generate a new Ethereum wallet with mnemonic phrase, private key, and address:

```bash
python generate_wallet.py
```

This will:
- Generate a secure 12-word BIP39 mnemonic phrase
- Create corresponding private key and Ethereum address
- Save credentials to `wallet.properties` file
- Display the wallet information in the terminal

The `wallet.properties` file will contain:
```
PRIV_KEY=0x...
ADDRESS=0x...
MNEMONIC=word1 word2 ... word12
```

## YouTube View Count Scraper

### Usage

Get the view count for a YouTube video by providing the video ID:

```bash
python get_viewcount.py VIDEO_ID
```

Example:
```bash
python get_viewcount.py dQw4w9WgXcQ
```

This will output the current view count as a number. If the video cannot be found or accessed, an error message will be displayed.

## Monitor Loop

The `monitor_loop` function continuously monitors YouTube view counts and updates the on-chain oracle when changes are detected:

- Periodically checks the current view count for a specified video
- Compares against the last recorded count stored in the blockchain
- Updates the on-chain oracle contract with the new view count when a change is detected
- Maintains synchronization between YouTube's real-time data and blockchain state
