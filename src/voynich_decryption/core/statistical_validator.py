"""Statistical validation engine for Voynich manuscript analysis."""

import logging

import numpy as np
from scipy import stats

from voynich_decryption.models import AnalysisResult

logger = logging.getLogger(__name__)


class StatisticalValidator:
    """
    Advanced statistical validation for morphemic analysis.

    This class provides comprehensive statistical tests to validate
    the morphemic decomposition results and assess their significance.
    """

    def __init__(self, significance_threshold: float = 0.05) -> None:
        """
        Initialize the statistical validator.

        Args:
            significance_threshold: P-value threshold for statistical significance
                                   (default: 0.05 for 95% confidence)

        Raises:
            ValueError: If significance threshold is not between 0 and 1
        """
        if not 0 < significance_threshold < 1:
            raise ValueError(
                f"Significance threshold must be between 0 and 1, got {significance_threshold}"
            )
        self.significance_threshold = significance_threshold
        logger.debug(f"StatisticalValidator initialized with α = {significance_threshold}")

    def validate_morphemic_patterns(self, analysis: AnalysisResult) -> dict[str, any]:
        """
        Perform comprehensive statistical validation of morphemic patterns.

        Args:
            analysis: Analysis results to validate

        Returns:
            Dictionary containing validation results and metrics

        Raises:
            ValueError: If analysis is invalid or contains no data
        """
        if not analysis.morpheme_inventory:
            logger.warning("No morphemes in inventory - using unknown morphemes from analysis")
            # Build inventory from word analyses
            temp_inventory = {}
            for wa in analysis.word_analyses:
                for m in wa.morphemes:
                    if m.morpheme_id not in temp_inventory:
                        temp_inventory[m.morpheme_id] = m
            analysis.morpheme_inventory = temp_inventory
            analysis.morphemes_identified = len(temp_inventory)

        logger.info("Performing statistical validation...")

        validation_results = {
            "chi_square_test": self._validate_chi_square(analysis),
            "distribution_analysis": self._analyze_distribution(analysis),
            "confidence_metrics": self._calculate_confidence_metrics(analysis),
            "frequency_analysis": self._analyze_frequencies(analysis),
            "morpheme_diversity": self._calculate_diversity_metrics(analysis),
        }

        logger.info("Statistical validation complete")
        return validation_results

    def _validate_chi_square(self, analysis: AnalysisResult) -> dict[str, any]:
        """
        Validate chi-square test results.

        Args:
            analysis: Analysis results

        Returns:
            Dictionary with chi-square validation results
        """
        is_significant = analysis.p_value < self.significance_threshold

        return {
            "statistic": float(analysis.chi_square_statistic),
            "p_value": float(analysis.p_value),
            "threshold": float(self.significance_threshold),
            "significant": is_significant,
            "interpretation": (
                "Non-random morpheme distribution (reject null hypothesis)"
                if is_significant
                else "Cannot reject random distribution hypothesis"
            ),
            "confidence_level": f"{(1 - self.significance_threshold) * 100:.1f}%",
        }

    def _analyze_distribution(self, analysis: AnalysisResult) -> dict[str, any]:
        """
        Analyze morpheme frequency distribution.

        Args:
            analysis: Analysis results

        Returns:
            Dictionary with distribution analysis results
        """
        frequencies = np.array([m.frequency for m in analysis.morpheme_inventory.values()])

        if len(frequencies) == 0:
            return {
                "error": "No morpheme frequencies available",
                "total_morphemes": 0,
            }

        return {
            "total_morphemes": len(frequencies),
            "mean_frequency": float(np.mean(frequencies)),
            "median_frequency": float(np.median(frequencies)),
            "std_frequency": float(np.std(frequencies)),
            "variance": float(np.var(frequencies)),
            "min_frequency": int(np.min(frequencies)),
            "max_frequency": int(np.max(frequencies)),
            "quartiles": {
                "q1": float(np.percentile(frequencies, 25)),
                "q2": float(np.percentile(frequencies, 50)),
                "q3": float(np.percentile(frequencies, 75)),
            },
            "coefficient_of_variation": (
                float(np.std(frequencies) / np.mean(frequencies))
                if np.mean(frequencies) > 0
                else 0.0
            ),
        }

    def _calculate_confidence_metrics(self, analysis: AnalysisResult) -> dict[str, any]:
        """
        Calculate confidence score metrics.

        Args:
            analysis: Analysis results

        Returns:
            Dictionary with confidence metrics
        """
        confidence_scores = np.array(
            [m.confidence_score for m in analysis.morpheme_inventory.values()]
        )

        if len(confidence_scores) == 0:
            return {
                "error": "No confidence scores available",
            }

        # Calculate confidence levels distribution
        high_confidence = np.sum(confidence_scores >= 0.7)
        medium_confidence = np.sum((confidence_scores >= 0.4) & (confidence_scores < 0.7))
        low_confidence = np.sum(confidence_scores < 0.4)

        return {
            "average_confidence": float(np.mean(confidence_scores)),
            "median_confidence": float(np.median(confidence_scores)),
            "std_confidence": float(np.std(confidence_scores)),
            "min_confidence": float(np.min(confidence_scores)),
            "max_confidence": float(np.max(confidence_scores)),
            "confidence_distribution": {
                "high (≥0.7)": int(high_confidence),
                "medium (0.4-0.7)": int(medium_confidence),
                "low (<0.4)": int(low_confidence),
            },
            "confidence_distribution_percentages": {
                "high": float(high_confidence / len(confidence_scores) * 100),
                "medium": float(medium_confidence / len(confidence_scores) * 100),
                "low": float(low_confidence / len(confidence_scores) * 100),
            },
        }

    def _analyze_frequencies(self, analysis: AnalysisResult) -> dict[str, any]:
        """
        Perform detailed frequency analysis.

        Args:
            analysis: Analysis results

        Returns:
            Dictionary with frequency analysis results
        """
        frequencies = np.array([m.frequency for m in analysis.morpheme_inventory.values()])

        if len(frequencies) < 2:
            return {
                "error": "Insufficient data for frequency analysis",
            }

        # Perform normality test (Shapiro-Wilk)
        try:
            shapiro_stat, shapiro_p = stats.shapiro(frequencies)
            is_normal = shapiro_p > self.significance_threshold
        except Exception as e:
            logger.warning(f"Shapiro-Wilk test failed: {e}")
            shapiro_stat, shapiro_p = None, None
            is_normal = False

        # Calculate skewness and kurtosis
        skewness = float(stats.skew(frequencies))
        kurtosis = float(stats.kurtosis(frequencies))

        return {
            "normality_test": {
                "test": "Shapiro-Wilk",
                "statistic": float(shapiro_stat) if shapiro_stat else None,
                "p_value": float(shapiro_p) if shapiro_p else None,
                "is_normal": is_normal,
            },
            "skewness": skewness,
            "skewness_interpretation": (
                "Right-skewed (long tail on right)"
                if skewness > 0.5
                else (
                    "Left-skewed (long tail on left)"
                    if skewness < -0.5
                    else "Approximately symmetric"
                )
            ),
            "kurtosis": kurtosis,
            "kurtosis_interpretation": (
                "Heavy-tailed (more outliers)" if kurtosis > 0 else "Light-tailed (fewer outliers)"
            ),
        }

    def _calculate_diversity_metrics(self, analysis: AnalysisResult) -> dict[str, any]:
        """
        Calculate morpheme diversity metrics.

        Args:
            analysis: Analysis results

        Returns:
            Dictionary with diversity metrics
        """
        frequencies = np.array([m.frequency for m in analysis.morpheme_inventory.values()])

        if len(frequencies) == 0:
            return {
                "error": "No morphemes available for diversity calculation",
            }

        total_occurrences = np.sum(frequencies)

        # Calculate Shannon entropy (diversity index)
        if total_occurrences > 0:
            proportions = frequencies / total_occurrences
            # Filter out zero proportions to avoid log(0)
            proportions = proportions[proportions > 0]
            shannon_entropy = -float(np.sum(proportions * np.log2(proportions)))
            max_entropy = np.log2(len(frequencies))
            evenness = shannon_entropy / max_entropy if max_entropy > 0 else 0.0
        else:
            shannon_entropy = 0.0
            max_entropy = 0.0
            evenness = 0.0

        # Simpson's diversity index
        if total_occurrences > 0:
            simpson_d = float(np.sum((frequencies / total_occurrences) ** 2))
            simpson_reciprocal = 1 / simpson_d if simpson_d > 0 else 0.0
        else:
            simpson_d = 0.0
            simpson_reciprocal = 0.0

        return {
            "unique_morphemes": len(frequencies),
            "total_occurrences": int(total_occurrences),
            "shannon_entropy": float(shannon_entropy),
            "max_possible_entropy": float(max_entropy) if total_occurrences > 0 else 0.0,
            "evenness": float(evenness),
            "simpson_diversity": float(simpson_d),
            "simpson_reciprocal": float(simpson_reciprocal),
            "interpretation": {
                "shannon": (
                    "High diversity (morphemes well-distributed)"
                    if shannon_entropy > max_entropy * 0.7
                    else "Low diversity (few morphemes dominate)"
                ),
                "evenness": (
                    "Even distribution"
                    if evenness > 0.7
                    else "Uneven distribution (some morphemes dominate)"
                ),
            },
        }

    def generate_validation_report(self, validation_results: dict[str, any]) -> str:
        """
        Generate a human-readable validation report.

        Args:
            validation_results: Results from validate_morphemic_patterns()

        Returns:
            Formatted validation report string
        """
        lines = [
            "=" * 70,
            "STATISTICAL VALIDATION REPORT",
            "=" * 70,
            "",
        ]

        # Chi-square test
        if "chi_square_test" in validation_results:
            chi = validation_results["chi_square_test"]
            lines.extend(
                [
                    "Chi-Square Test:",
                    f"  Statistic:      {chi.get('statistic', 0):.4f}",
                    f"  P-Value:        {chi.get('p_value', 1):.6f}",
                    f"  Threshold:      {chi.get('threshold', 0.05):.3f}",
                    f"  Significant:    {'YES' if chi.get('significant', False) else 'NO'}",
                    f"  Interpretation: {chi.get('interpretation', 'N/A')}",
                    "",
                ]
            )

        # Distribution analysis
        if "distribution_analysis" in validation_results:
            dist = validation_results["distribution_analysis"]
            lines.extend(
                [
                    "Frequency Distribution:",
                    f"  Mean:      {dist.get('mean_frequency', 0):.2f}",
                    f"  Median:    {dist.get('median_frequency', 0):.2f}",
                    f"  Std Dev:   {dist.get('std_frequency', 0):.2f}",
                    f"  Min:       {dist.get('min_frequency', 0)}",
                    f"  Max:       {dist.get('max_frequency', 0)}",
                    "",
                ]
            )

        # Confidence metrics
        if "confidence_metrics" in validation_results:
            conf = validation_results["confidence_metrics"]
            lines.extend(
                [
                    "Confidence Metrics:",
                    f"  Average:   {conf.get('average_confidence', 0):.2%}",
                    f"  High:      {conf.get('confidence_distribution', {}).get('high (≥0.7)', 0)} morphemes",
                    f"  Medium:    {conf.get('confidence_distribution', {}).get('medium (0.4-0.7)', 0)} morphemes",
                    f"  Low:       {conf.get('confidence_distribution', {}).get('low (<0.4)', 0)} morphemes",
                    "",
                ]
            )

        # Diversity metrics
        if "morpheme_diversity" in validation_results:
            div = validation_results["morpheme_diversity"]
            lines.extend(
                [
                    "Diversity Metrics:",
                    f"  Shannon Entropy: {div.get('shannon_entropy', 0):.4f}",
                    f"  Evenness:        {div.get('evenness', 0):.2%}",
                    f"  Interpretation:  {div.get('interpretation', {}).get('shannon', 'N/A')}",
                    "",
                ]
            )

        lines.append("=" * 70)

        return "\n".join(lines)
