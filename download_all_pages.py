#!/usr/bin/env python3
"""
Download all 214 pages of the Voynich Manuscript from Yale University Library.
Pages are numbered: 1r, 1v, 2r, 2v, ..., 116v (total 234 folio sides, some missing)
"""

import requests
import os
import time
from pathlib import Path

# Create directory
output_dir = Path("images/pages")
output_dir.mkdir(parents=True, exist_ok=True)

# Yale Beinecke Library - High resolution images
# Format: https://brbl-dl.library.yale.edu/vufind/Record/3519597/Image?id=1&size=full

BASE_URL = "https://brbl-dl.library.yale.edu/vufind/Record/3519597"

def download_page(page_num, output_path):
    """Download a single page from Yale library."""
    url = f"{BASE_URL}/Image?id={page_num}&size=full"

    try:
        print(f"Downloading page {page_num}...", end=" ")
        response = requests.get(url, timeout=30, stream=True)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✓ Saved to {output_path}")
            return True
        else:
            print(f"✗ Failed (status {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Download all 214 pages of the Voynich Manuscript."""

    print("="*60)
    print("Voynich Manuscript - Complete Page Download")
    print("Source: Yale Beinecke Rare Book & Manuscript Library")
    print("="*60)

    # The manuscript has pages from ~1 to ~234 (some are missing)
    # We'll try all and skip 404s
    total_downloaded = 0
    total_failed = 0

    for page_num in range(1, 235):  # Try pages 1-234
        output_file = output_dir / f"page_{page_num:03d}.jpg"

        # Skip if already exists
        if output_file.exists():
            file_size = output_file.stat().st_size
            if file_size > 10000:  # At least 10KB
                print(f"Page {page_num:03d} already exists ({file_size:,} bytes), skipping")
                total_downloaded += 1
                continue

        # Download
        success = download_page(page_num, output_file)

        if success:
            total_downloaded += 1
        else:
            total_failed += 1
            # Remove failed download
            if output_file.exists() and output_file.stat().st_size < 10000:
                output_file.unlink()

        # Be nice to the server
        time.sleep(0.5)

    print("\n" + "="*60)
    print(f"Download complete!")
    print(f"✓ Successfully downloaded: {total_downloaded} pages")
    print(f"✗ Failed/Missing: {total_failed} pages")
    print(f"Output directory: {output_dir.absolute()}")
    print("="*60)

if __name__ == "__main__":
    main()
