"""Report generation pipeline for Voynich manuscript analysis."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from voynich_decryption.models import AnalysisResult

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generate comprehensive analysis reports in multiple formats.

    This class handles the generation of analysis reports in various
    formats including JSON, CSV, HTML, and plain text.
    """

    def __init__(self, output_dir: Optional[str] = None) -> None:
        """
        Initialize the report generator.

        Args:
            output_dir: Optional output directory for reports (default: ./output)
        """
        self.output_dir = Path(output_dir) if output_dir else Path("./output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"ReportGenerator initialized with output_dir: {self.output_dir}")

    def generate_json_report(
        self,
        analysis: AnalysisResult,
        output_file: Optional[str] = None,
    ) -> Path:
        """
        Generate comprehensive JSON report.

        Args:
            analysis: Analysis results to report
            output_file: Optional output filename (default: analysis_results.json)

        Returns:
            Path to generated report file

        Raises:
            IOError: If file cannot be written
        """
        if output_file is None:
            output_file = "analysis_results.json"

        output_path = self.output_dir / output_file

        try:
            report_data = {
                "metadata": {
                    "title": "Voynich Manuscript Morphemic Analysis",
                    "generated_at": datetime.now().isoformat(),
                    "version": "1.0.0",
                    "total_words_analyzed": analysis.total_words_analyzed,
                    "total_unique_words": analysis.total_unique_words,
                    "morphemes_identified": analysis.morphemes_identified,
                },
                "statistical_results": {
                    "chi_square_statistic": float(analysis.chi_square_statistic),
                    "p_value": float(analysis.p_value),
                    "significance_threshold": float(
                        analysis.statistical_significance_threshold
                    ),
                    "statistically_significant": analysis.is_statistically_significant,
                },
                "summary": {
                    "verified_words": analysis.verified_words_count,
                    "average_confidence": float(analysis.average_word_confidence),
                    "high_confidence_words": len(analysis.high_confidence_words),
                },
                "morpheme_inventory": {
                    mid: m.to_dict() for mid, m in analysis.morpheme_inventory.items()
                },
                "word_analyses": [wa.to_dict() for wa in analysis.word_analyses],
            }

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)

            logger.info(f"JSON report generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate JSON report: {e}")
            raise IOError(f"Failed to generate JSON report: {e}") from e

    def generate_csv_report(
        self,
        analysis: AnalysisResult,
        output_file: Optional[str] = None,
    ) -> Path:
        """
        Generate CSV report of morpheme inventory.

        Args:
            analysis: Analysis results to report
            output_file: Optional output filename (default: morpheme_inventory.csv)

        Returns:
            Path to generated report file

        Raises:
            IOError: If file cannot be written
        """
        if output_file is None:
            output_file = "morpheme_inventory.csv"

        output_path = self.output_dir / output_file

        try:
            # Convert morpheme inventory to DataFrame
            data = []
            for morpheme_id, morpheme in analysis.morpheme_inventory.items():
                data.append({
                    "morpheme_id": morpheme_id,
                    "glyph": morpheme.glyph,
                    "type": morpheme.morpheme_type.value,
                    "frequency": morpheme.frequency,
                    "confidence_score": morpheme.confidence_score,
                    "botanical_reference": morpheme.botanical_reference or "",
                    "pharmaceutical_use": morpheme.pharmaceutical_use or "",
                    "related_morphemes": ",".join(morpheme.related_morphemes),
                })

            df = pd.DataFrame(data)

            # Sort by frequency (descending)
            df = df.sort_values("frequency", ascending=False)

            df.to_csv(output_path, index=False, encoding="utf-8")

            logger.info(f"CSV report generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate CSV report: {e}")
            raise IOError(f"Failed to generate CSV report: {e}") from e

    def generate_text_report(
        self,
        analysis: AnalysisResult,
        output_file: Optional[str] = None,
    ) -> Path:
        """
        Generate plain text summary report.

        Args:
            analysis: Analysis results to report
            output_file: Optional output filename (default: analysis_summary.txt)

        Returns:
            Path to generated report file

        Raises:
            IOError: If file cannot be written
        """
        if output_file is None:
            output_file = "analysis_summary.txt"

        output_path = self.output_dir / output_file

        try:
            report_text = analysis.get_summary_report()

            # Add additional sections
            report_text += "\n\n"
            report_text += self._generate_top_morphemes_section(analysis)
            report_text += "\n\n"
            report_text += self._generate_confidence_breakdown(analysis)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report_text)

            logger.info(f"Text report generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate text report: {e}")
            raise IOError(f"Failed to generate text report: {e}") from e

    def generate_word_analysis_report(
        self,
        analysis: AnalysisResult,
        output_file: Optional[str] = None,
    ) -> Path:
        """
        Generate detailed CSV report of word analyses.

        Args:
            analysis: Analysis results to report
            output_file: Optional output filename (default: word_analyses.csv)

        Returns:
            Path to generated report file

        Raises:
            IOError: If file cannot be written
        """
        if output_file is None:
            output_file = "word_analyses.csv"

        output_path = self.output_dir / output_file

        try:
            data = []
            for word_analysis in analysis.word_analyses:
                data.append({
                    "word_id": word_analysis.word_id,
                    "word_glyph": word_analysis.word_glyph,
                    "morpheme_count": word_analysis.morpheme_count,
                    "total_frequency": word_analysis.total_frequency,
                    "confidence": word_analysis.confidence,
                    "average_morpheme_confidence": word_analysis.average_morpheme_confidence,
                    "verification_status": word_analysis.verification_status,
                    "potential_meaning": word_analysis.potential_meaning or "",
                    "morphemes": " + ".join(m.glyph for m in word_analysis.morphemes),
                })

            df = pd.DataFrame(data)

            # Sort by confidence (descending)
            df = df.sort_values("confidence", ascending=False)

            df.to_csv(output_path, index=False, encoding="utf-8")

            logger.info(f"Word analysis report generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate word analysis report: {e}")
            raise IOError(f"Failed to generate word analysis report: {e}") from e

    def generate_all_reports(self, analysis: AnalysisResult) -> dict[str, Path]:
        """
        Generate all report formats.

        Args:
            analysis: Analysis results to report

        Returns:
            Dictionary mapping report type to file path
        """
        logger.info("Generating all report formats...")

        reports = {
            "json": self.generate_json_report(analysis),
            "csv_morphemes": self.generate_csv_report(analysis),
            "csv_words": self.generate_word_analysis_report(analysis),
            "text": self.generate_text_report(analysis),
        }

        logger.info(f"Generated {len(reports)} reports in {self.output_dir}")
        return reports

    def _generate_top_morphemes_section(
        self, analysis: AnalysisResult, top_n: int = 20
    ) -> str:
        """Generate section showing top morphemes by frequency."""
        lines = [
            f"Top {top_n} Most Frequent Morphemes:",
            "=" * 70,
            f"{'Rank':<6} {'Glyph':<15} {'Type':<12} {'Frequency':<12} {'Confidence':<12}",
            "-" * 70,
        ]

        # Sort morphemes by frequency
        sorted_morphemes = sorted(
            analysis.morpheme_inventory.values(),
            key=lambda m: m.frequency,
            reverse=True,
        )[:top_n]

        for rank, morpheme in enumerate(sorted_morphemes, 1):
            lines.append(
                f"{rank:<6} {morpheme.glyph:<15} {morpheme.morpheme_type.value:<12} "
                f"{morpheme.frequency:<12} {morpheme.confidence_score:<12.2f}"
            )

        lines.append("=" * 70)
        return "\n".join(lines)

    def _generate_confidence_breakdown(self, analysis: AnalysisResult) -> str:
        """Generate confidence score breakdown section."""
        high_conf = [wa for wa in analysis.word_analyses if wa.confidence >= 0.7]
        med_conf = [wa for wa in analysis.word_analyses if 0.4 <= wa.confidence < 0.7]
        low_conf = [wa for wa in analysis.word_analyses if wa.confidence < 0.4]

        total = len(analysis.word_analyses)

        lines = [
            "Confidence Score Breakdown:",
            "=" * 70,
            f"High Confidence (≥0.7):   {len(high_conf):>6} ({len(high_conf)/total*100:>5.1f}%)",
            f"Medium Confidence (0.4-0.7): {len(med_conf):>6} ({len(med_conf)/total*100:>5.1f}%)",
            f"Low Confidence (<0.4):    {len(low_conf):>6} ({len(low_conf)/total*100:>5.1f}%)",
            "=" * 70,
        ]

        return "\n".join(lines)
