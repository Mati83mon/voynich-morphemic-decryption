#!/usr/bin/env python3
"""
Convert Voynich top 100 words CSV to JSON format.

This script converts the CSV file containing top 100 words into
a structured JSON format suitable for analysis.
"""

import csv
import json
import sys
from pathlib import Path


def convert_top100_to_json(
    csv_file: str,
    output_json: str,
    vocabulary_json: str,
) -> None:
    """
    Convert top 100 words CSV to JSON formats.

    Creates two JSON files:
    1. Detailed analysis format with all metadata
    2. Simple vocabulary format (word_id -> word_glyph) for analysis

    Args:
        csv_file: Path to input CSV file
        output_json: Path to output detailed JSON file
        vocabulary_json: Path to output vocabulary JSON file
    """
    csv_path = Path(csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    # Read CSV
    words_data = []
    vocabulary = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            word = row["Word"]
            frequency = int(row["Frequency"])
            percentage = float(row["Percentage"])
            length = int(row["Length"])

            # Create detailed entry
            word_entry = {
                "word_id": f"top_{idx:03d}",
                "word": word,
                "frequency": frequency,
                "percentage": percentage,
                "length": length,
                "rank": idx,
            }
            words_data.append(word_entry)

            # Create vocabulary entry
            vocabulary[f"top_{idx:03d}"] = word

    # Save detailed JSON
    detailed_data = {
        "metadata": {
            "source": "Voynich Manuscript",
            "description": "Top 100 most frequent words",
            "total_words": len(words_data),
            "format_version": "1.0",
        },
        "words": words_data,
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(detailed_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Created detailed JSON: {output_json}")
    print(f"  Total words: {len(words_data)}")

    # Save vocabulary JSON
    with open(vocabulary_json, "w", encoding="utf-8") as f:
        json.dump(vocabulary, f, indent=2, ensure_ascii=False)

    print(f"✓ Created vocabulary JSON: {vocabulary_json}")
    print(f"  Total entries: {len(vocabulary)}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("CSV to JSON Converter - Voynich Top 100 Words")
    print("=" * 70)
    print()

    # Define paths
    csv_file = "data/processed/voynich_top_100_words.csv"
    output_json = "data/processed/voynich_top_100_detailed.json"
    vocabulary_json = "data/processed/voynich_top_100_vocabulary.json"

    try:
        convert_top100_to_json(csv_file, output_json, vocabulary_json)
        print()
        print("=" * 70)
        print("Conversion complete!")
        print("=" * 70)

    except Exception as e:
        print(f"ERROR: Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
