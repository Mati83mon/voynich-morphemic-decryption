"""Complete analysis pipeline for Voynich manuscript."""

import json
import logging
from pathlib import Path
from typing import Optional

from voynich_decryption.core import MorphemicAnalyzer, StatisticalValidator
from voynich_decryption.models import AnalysisResult
from voynich_decryption.pipelines.reporting_pipeline import ReportGenerator

logger = logging.getLogger(__name__)


class VoynichAnalysisPipeline:
    """
    Complete Voynich manuscript analysis pipeline.

    This class orchestrates the entire analysis workflow, from data loading
    through morphemic analysis, statistical validation, and report generation.

    Attributes:
        config: Pipeline configuration dictionary
        analyzer: MorphemicAnalyzer instance
        validator: StatisticalValidator instance
        reporter: ReportGenerator instance
    """

    def __init__(self, config: Optional[dict[str, any]] = None) -> None:
        """
        Initialize the analysis pipeline.

        Args:
            config: Optional configuration dictionary with following keys:
                - significance_threshold: float (default: 0.05)
                - output_dir: str (default: ./output)
                - verbose: bool (default: True)
                - enable_caching: bool (default: True)
        """
        self.config = config or {}

        # Extract configuration parameters
        significance_threshold = self.config.get("significance_threshold", 0.05)
        output_dir = self.config.get("output_dir", "./output")
        verbose = self.config.get("verbose", True)

        # Initialize components
        self.analyzer = MorphemicAnalyzer(verbose=verbose)
        self.validator = StatisticalValidator(
            significance_threshold=significance_threshold
        )
        self.reporter = ReportGenerator(output_dir=output_dir)

        logger.info("VoynichAnalysisPipeline initialized successfully")
        logger.debug(f"Configuration: {self.config}")

    def execute(
        self,
        vocabulary_file: str,
        morpheme_inventory_file: Optional[str] = None,
        generate_reports: bool = True,
    ) -> AnalysisResult:
        """
        Execute complete analysis pipeline.

        This method performs the following steps:
        1. Load vocabulary data
        2. Load morpheme inventory (if provided)
        3. Perform morphemic analysis
        4. Validate results statistically
        5. Generate reports (if enabled)

        Args:
            vocabulary_file: Path to vocabulary JSON file (word_id -> word_glyph)
            morpheme_inventory_file: Optional path to morpheme inventory JSON
            generate_reports: Whether to generate output reports (default: True)

        Returns:
            Complete analysis results

        Raises:
            FileNotFoundError: If vocabulary file doesn't exist
            ValueError: If vocabulary file has invalid format
            IOError: If report generation fails
        """
        logger.info("=" * 70)
        logger.info("Starting Voynich Manuscript Analysis Pipeline")
        logger.info("=" * 70)

        # Step 1: Load morpheme inventory (if provided)
        if morpheme_inventory_file:
            logger.info(f"Loading morpheme inventory from: {morpheme_inventory_file}")
            self.analyzer.load_vocabulary(morpheme_inventory_file)
        else:
            logger.info("No morpheme inventory provided, starting with empty inventory")

        # Step 2: Load vocabulary
        logger.info(f"Loading vocabulary from: {vocabulary_file}")
        vocabulary = self._load_vocabulary(vocabulary_file)
        logger.info(f"Loaded {len(vocabulary)} words")

        # Step 3: Perform morphemic analysis
        logger.info("Performing morphemic analysis...")
        analysis = self.analyzer.analyze_vocabulary(vocabulary)
        logger.info(
            f"Analysis complete: {analysis.morphemes_identified} morphemes identified"
        )

        # Step 4: Statistical validation
        logger.info("Performing statistical validation...")
        validation_results = self.validator.validate_morphemic_patterns(analysis)
        logger.info(
            f"Validation complete: "
            f"{'Significant' if analysis.is_statistically_significant else 'Not significant'}"
        )

        # Add validation results to analysis metadata
        analysis.metadata["validation_results"] = validation_results

        # Step 5: Generate reports (if enabled)
        if generate_reports:
            logger.info("Generating analysis reports...")
            report_paths = self.reporter.generate_all_reports(analysis)
            logger.info(f"Generated {len(report_paths)} reports")
            analysis.metadata["report_paths"] = {
                k: str(v) for k, v in report_paths.items()
            }

        # Step 6: Log summary
        self._log_summary(analysis, validation_results)

        logger.info("=" * 70)
        logger.info("Pipeline execution complete!")
        logger.info("=" * 70)

        return analysis

    def execute_from_config_file(self, config_file: str) -> AnalysisResult:
        """
        Execute pipeline using configuration from JSON/YAML file.

        Args:
            config_file: Path to configuration file

        Returns:
            Analysis results

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file has invalid format
        """
        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        logger.info(f"Loading configuration from: {config_file}")

        if config_path.suffix == ".json":
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        elif config_path.suffix in [".yaml", ".yml"]:
            import yaml
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        else:
            raise ValueError(
                f"Unsupported config file format: {config_path.suffix}. "
                "Use .json, .yaml, or .yml"
            )

        # Update pipeline configuration
        self.config.update(config.get("pipeline", {}))

        # Execute pipeline
        return self.execute(
            vocabulary_file=config["vocabulary_file"],
            morpheme_inventory_file=config.get("morpheme_inventory_file"),
            generate_reports=config.get("generate_reports", True),
        )

    def _load_vocabulary(self, filepath: str) -> dict[str, str]:
        """
        Load vocabulary from JSON file.

        Args:
            filepath: Path to vocabulary JSON file

        Returns:
            Dictionary mapping word_id to word_glyph

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file has invalid format
        """
        vocab_path = Path(filepath)

        if not vocab_path.exists():
            raise FileNotFoundError(f"Vocabulary file not found: {filepath}")

        try:
            with open(vocab_path, "r", encoding="utf-8") as f:
                vocabulary = json.load(f)

            if not isinstance(vocabulary, dict):
                raise ValueError("Vocabulary file must contain a JSON object")

            # Validate vocabulary format
            for word_id, word_glyph in vocabulary.items():
                if not isinstance(word_glyph, str):
                    logger.warning(
                        f"Invalid word glyph for '{word_id}': {word_glyph}"
                    )

            return vocabulary

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in vocabulary file: {e}") from e
        except Exception as e:
            logger.error(f"Failed to load vocabulary: {e}")
            raise

    def _log_summary(
        self, analysis: AnalysisResult, validation_results: dict[str, any]
    ) -> None:
        """Log a summary of analysis results."""
        logger.info("")
        logger.info("Analysis Summary:")
        logger.info(f"  Total words analyzed:      {analysis.total_words_analyzed:,}")
        logger.info(f"  Unique words:              {analysis.total_unique_words:,}")
        logger.info(f"  Morphemes identified:      {analysis.morphemes_identified:,}")
        logger.info(f"  Verified words:            {analysis.verified_words_count:,}")
        logger.info(f"  Average word confidence:   {analysis.average_word_confidence:.2%}")
        logger.info("")
        logger.info("Statistical Results:")
        logger.info(f"  Chi-square statistic:      {analysis.chi_square_statistic:.4f}")
        logger.info(f"  P-value:                   {analysis.p_value:.6f}")
        logger.info(
            f"  Statistically significant: "
            f"{'YES' if analysis.is_statistically_significant else 'NO'}"
        )
        logger.info("")

        # Log confidence breakdown
        if "confidence_metrics" in validation_results:
            conf = validation_results["confidence_metrics"]
            dist = conf.get("confidence_distribution", {})
            logger.info("Confidence Distribution:")
            logger.info(f"  High (≥0.7):    {dist.get('high (≥0.7)', 0):,}")
            logger.info(f"  Medium (0.4-0.7): {dist.get('medium (0.4-0.7)', 0):,}")
            logger.info(f"  Low (<0.4):     {dist.get('low (<0.4)', 0):,}")

    def clear_cache(self) -> None:
        """Clear analyzer cache."""
        self.analyzer.clear_cache()
        logger.info("Pipeline cache cleared")

    def get_statistics(self) -> dict[str, any]:
        """
        Get pipeline statistics.

        Returns:
            Dictionary containing pipeline statistics
        """
        return {
            "pipeline_config": self.config,
            "analyzer_stats": self.analyzer.get_statistics(),
        }
