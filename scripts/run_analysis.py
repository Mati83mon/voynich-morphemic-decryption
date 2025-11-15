#!/usr/bin/env python3
"""
Main analysis script for Voynich Morphemic Decryption.

This script runs the complete analysis pipeline.
"""

import logging
import sys
from pathlib import Path

from voynich_decryption import VoynichAnalysisPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    logger.info("=" * 70)
    logger.info("Voynich Morphemic Decryption - Analysis Pipeline")
    logger.info("=" * 70)

    # Define file paths
    data_dir = Path("data")
    vocabulary_file = data_dir / "voynich_full_vocabulary.json"
    morpheme_inventory_file = data_dir / "processed" / "morpheme_analysis_complete.json"
    output_dir = Path("output")

    # Check if vocabulary file exists
    if not vocabulary_file.exists():
        logger.error(f"Vocabulary file not found: {vocabulary_file}")
        logger.error("Please ensure the vocabulary file exists in the data directory.")
        sys.exit(1)

    # Initialize pipeline
    config = {
        "significance_threshold": 0.05,
        "output_dir": str(output_dir),
        "verbose": True,
    }

    pipeline = VoynichAnalysisPipeline(config=config)

    # Execute pipeline
    try:
        logger.info("Starting analysis...")

        result = pipeline.execute(
            vocabulary_file=str(vocabulary_file),
            morpheme_inventory_file=(
                str(morpheme_inventory_file)
                if morpheme_inventory_file.exists()
                else None
            ),
            generate_reports=True,
        )

        logger.info("")
        logger.info("=" * 70)
        logger.info("ANALYSIS COMPLETE!")
        logger.info("=" * 70)
        logger.info("")
        logger.info(result.get_summary_report())

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
