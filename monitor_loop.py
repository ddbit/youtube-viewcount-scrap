import time
import argparse
from web3 import Web3
from Performance import ContractPerformance
from get_viewcount import get_video_views

def video_id_to_key(video_id):
    """Convert video ID to keccak256 hash key"""
    video_id_bytes = video_id.encode('utf-8')
    key_hash = Web3.keccak(video_id_bytes)
    return key_hash.hex()

def monitor_and_update(video_id, loop_time):
    """Monitor video views and update contract if changed"""
    print(f"Starting monitor for video ID: {video_id}")
    print(f"Loop interval: {loop_time} seconds")
    
    # Initialize contract interface
    try:
        perf = ContractPerformance()
    except Exception as e:
        print(f"Error initializing contract: {e}")
        return False
    
    # Generate key from video ID
    key_hex = video_id_to_key(video_id)
    print(f"Using key: {key_hex}")
    
    while True:
        try:
            print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Checking video views...")
            
            # Get current view count from YouTube
            current_views = get_video_views(video_id)
            if current_views is None:
                print("Failed to get view count, skipping update")
                time.sleep(loop_time)
                continue
            
            print(f"Current YouTube views: {current_views}")
            
            # Get current indicator from contract
            try:
                contract_indicator = perf.get_indicator(key_hex)
                if contract_indicator is None:
                    contract_indicator = 0  # Assume 0 if not set
                print(f"Contract indicator: {contract_indicator}")
            except Exception as e:
                print(f"Error getting contract indicator: {e}")
                contract_indicator = 0
            
            # Compare and update if different
            if current_views != contract_indicator:
                print(f"View count changed! Updating contract: {contract_indicator} -> {current_views}")
                
                try:
                    tx_hash = perf.set_indicator(key_hex, current_views)
                    if tx_hash:
                        print(f"Successfully updated contract. Transaction: {tx_hash}")
                    else:
                        print("Failed to update contract")
                except Exception as e:
                    print(f"Error updating contract: {e}")
            else:
                print("No change in view count, no update needed")
            
        except KeyboardInterrupt:
            print("\nStopping monitor...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        # Wait before next check
        print(f"Waiting {loop_time} seconds until next check...")
        time.sleep(loop_time)
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor YouTube video views and update Performance contract')
    parser.add_argument('video_id', type=str, help='YouTube video ID to monitor')
    parser.add_argument('--loop-time', type=int, default=300, help='Loop interval in seconds (default: 300 = 5 minutes)')
    
    args = parser.parse_args()
    
    print("YouTube View Count Monitor")
    print("=" * 30)
    print(f"This script will monitor YouTube video views every {args.loop_time} seconds")
    print("and update the Performance contract when views change.")
    print("Press Ctrl+C to stop.\n")
    
    monitor_and_update(args.video_id, args.loop_time)