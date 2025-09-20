#!/usr/bin/env python3
import sys
import urllib.request
import urllib.error
import re
import argparse
import ssl

PREFIX = 'https://www.youtube.com/watch?v='

def get_video_views(video_id):
    url = PREFIX + video_id
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(url, context=context) as response:
            html = response.read().decode('utf-8')
        
        m = re.search(r'"viewCount"\s*:\s*"(\d+)"', html)
        views = int(m.group(1)) if m else None
        return views
    except urllib.error.URLError as e:
        print(f"Error fetching video: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error parsing video data: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Get YouTube video view count')
    parser.add_argument('video_id', type=str, help='YouTube video ID')
    
    args = parser.parse_args()
    
    views = get_video_views(args.video_id)
    if views is not None:
        print(views)
        return 0
    else:
        print("Could not retrieve view count", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
