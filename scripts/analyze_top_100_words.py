#!/usr/bin/env python3
"""
Comprehensive analysis script for Voynich top 100 words.

This script performs morphemic analysis on the top 100 most frequent
words from the Voynich manuscript.
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voynich_decryption import (
    VoynichAnalysisPipeline,
    MorphemicAnalyzer,
    StatisticalValidator,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def load_top_100_vocabulary(vocab_file: str) -> dict[str, str]:
    """
    Load top 100 vocabulary from JSON file.

    Args:
        vocab_file: Path to vocabulary JSON file

    Returns:
        Dictionary mapping word_id to word_glyph
    """
    vocab_path = Path(vocab_file)
    if not vocab_path.exists():
        raise FileNotFoundError(f"Vocabulary file not found: {vocab_file}")

    with open(vocab_path, "r", encoding="utf-8") as f:
        vocabulary = json.load(f)

    logger.info(f"Loaded {len(vocabulary)} words from {vocab_file}")
    return vocabulary


def load_word_metadata(detailed_file: str) -> dict:
    """
    Load detailed word metadata.

    Args:
        detailed_file: Path to detailed JSON file

    Returns:
        Dictionary with metadata and word details
    """
    detailed_path = Path(detailed_file)
    if not detailed_path.exists():
        raise FileNotFoundError(f"Detailed file not found: {detailed_file}")

    with open(detailed_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info(f"Loaded metadata for {len(data['words'])} words")
    return data


def create_frequency_groups(words_data: list[dict]) -> dict:
    """
    Group words by frequency ranges.

    Args:
        words_data: List of word dictionaries with frequency data

    Returns:
        Dictionary with frequency groups
    """
    groups = {
        "very_high": [],  # > 100
        "high": [],       # 50-100
        "medium": [],     # 20-49
        "low": [],        # 10-19
        "very_low": [],   # < 10
    }

    for word in words_data:
        freq = word["frequency"]
        if freq > 100:
            groups["very_high"].append(word)
        elif freq >= 50:
            groups["high"].append(word)
        elif freq >= 20:
            groups["medium"].append(word)
        elif freq >= 10:
            groups["low"].append(word)
        else:
            groups["very_low"].append(word)

    return groups


def create_length_groups(words_data: list[dict]) -> dict:
    """
    Group words by length.

    Args:
        words_data: List of word dictionaries with length data

    Returns:
        Dictionary with length groups
    """
    groups = {}

    for word in words_data:
        length = word["length"]
        if length not in groups:
            groups[length] = []
        groups[length].append(word)

    return groups


def analyze_character_patterns(words_data: list[dict]) -> dict:
    """
    Analyze character patterns in words.

    Args:
        words_data: List of word dictionaries

    Returns:
        Dictionary with character pattern analysis
    """
    char_freq = {}
    char_positions = {"first": {}, "last": {}, "middle": {}}

    for word in words_data:
        word_text = word["word"]

        # Count all characters
        for char in word_text:
            char_freq[char] = char_freq.get(char, 0) + 1

        # Position analysis
        if word_text:
            # First character
            first_char = word_text[0]
            char_positions["first"][first_char] = (
                char_positions["first"].get(first_char, 0) + 1
            )

            # Last character
            last_char = word_text[-1]
            char_positions["last"][last_char] = (
                char_positions["last"].get(last_char, 0) + 1
            )

            # Middle characters
            if len(word_text) > 2:
                for char in word_text[1:-1]:
                    char_positions["middle"][char] = (
                        char_positions["middle"].get(char, 0) + 1
                    )

    # Sort by frequency
    sorted_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)

    return {
        "character_frequencies": dict(sorted_chars),
        "total_unique_chars": len(char_freq),
        "position_analysis": char_positions,
        "top_10_chars": dict(sorted_chars[:10]),
    }


def main():
    """Main execution function."""
    logger.info("=" * 70)
    logger.info("Voynich Top 100 Words - Comprehensive Analysis")
    logger.info("=" * 70)
    logger.info("")

    # Define paths
    vocabulary_file = "data/processed/voynich_top_100_vocabulary.json"
    detailed_file = "data/processed/voynich_top_100_detailed.json"
    morpheme_inventory_file = "data/processed/morpheme_analysis_complete.json"
    output_dir = Path("output/top_100_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Step 1: Load data
        logger.info("Step 1: Loading data...")
        vocabulary = load_top_100_vocabulary(vocabulary_file)
        detailed_data = load_word_metadata(detailed_file)
        words_data = detailed_data["words"]

        # Step 2: Preliminary analysis
        logger.info("Step 2: Performing preliminary analysis...")

        # Frequency groups
        freq_groups = create_frequency_groups(words_data)
        logger.info(f"  Very high frequency (>100): {len(freq_groups['very_high'])} words")
        logger.info(f"  High frequency (50-100): {len(freq_groups['high'])} words")
        logger.info(f"  Medium frequency (20-49): {len(freq_groups['medium'])} words")
        logger.info(f"  Low frequency (10-19): {len(freq_groups['low'])} words")
        logger.info(f"  Very low frequency (<10): {len(freq_groups['very_low'])} words")

        # Length groups
        length_groups = create_length_groups(words_data)
        logger.info(f"  Word length range: {min(length_groups.keys())}-{max(length_groups.keys())} characters")

        # Character patterns
        char_patterns = analyze_character_patterns(words_data)
        logger.info(f"  Unique characters: {char_patterns['total_unique_chars']}")
        logger.info(f"  Top 3 characters: {list(char_patterns['top_10_chars'].keys())[:3]}")

        # Step 3: Morphemic analysis
        logger.info("")
        logger.info("Step 3: Running morphemic analysis...")

        config = {
            "significance_threshold": 0.05,
            "output_dir": str(output_dir),
            "verbose": True,
        }

        pipeline = VoynichAnalysisPipeline(config=config)

        # Run analysis
        result = pipeline.execute(
            vocabulary_file=vocabulary_file,
            morpheme_inventory_file=(
                morpheme_inventory_file
                if Path(morpheme_inventory_file).exists()
                else None
            ),
            generate_reports=True,
        )

        # Step 4: Save comprehensive analysis
        logger.info("")
        logger.info("Step 4: Saving comprehensive analysis...")

        comprehensive_analysis = {
            "metadata": {
                "title": "Voynich Top 100 Words - Comprehensive Analysis",
                "analysis_date": datetime.now().isoformat(),
                "total_words": len(vocabulary),
                "source_file": vocabulary_file,
            },
            "preliminary_analysis": {
                "frequency_groups": {
                    k: len(v) for k, v in freq_groups.items()
                },
                "length_distribution": {
                    str(k): len(v) for k, v in length_groups.items()
                },
                "character_patterns": char_patterns,
            },
            "morphemic_analysis": {
                "total_words_analyzed": result.total_words_analyzed,
                "unique_words": result.total_unique_words,
                "morphemes_identified": result.morphemes_identified,
                "chi_square_statistic": float(result.chi_square_statistic),
                "p_value": float(result.p_value),
                "statistically_significant": result.is_statistically_significant,
                "average_confidence": float(result.average_word_confidence),
                "verified_words": result.verified_words_count,
            },
            "top_words": {
                "top_10_by_frequency": words_data[:10],
                "top_10_by_length": sorted(
                    words_data, key=lambda x: x["length"], reverse=True
                )[:10],
            },
        }

        # Save to JSON
        output_file = output_dir / "comprehensive_analysis.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(comprehensive_analysis, f, indent=2, ensure_ascii=False)

        logger.info(f"✓ Saved comprehensive analysis: {output_file}")

        # Step 5: Print summary
        logger.info("")
        logger.info("=" * 70)
        logger.info("ANALYSIS COMPLETE!")
        logger.info("=" * 70)
        logger.info("")
        logger.info(result.get_summary_report())

        logger.info("")
        logger.info(f"Output files saved to: {output_dir}")
        logger.info("  - comprehensive_analysis.json")
        logger.info("  - analysis_results.json")
        logger.info("  - morpheme_inventory.csv")
        logger.info("  - word_analyses.csv")
        logger.info("  - analysis_summary.txt")

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
