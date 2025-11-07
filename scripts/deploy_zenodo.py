#!/usr/bin/env python3
"""
Zenodo API Integration Script for Voynich Morphemic Decryption.

This script handles automatic deployment and publishing to Zenodo,
creating DOIs for research outputs.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ZenodoPublisher:
    """
    Handle publishing to Zenodo via REST API.

    Zenodo provides persistent identifiers (DOIs) for research outputs.
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        sandbox: bool = True,
    ) -> None:
        """
        Initialize Zenodo publisher.

        Args:
            access_token: Zenodo API access token (or from ZENODO_TOKEN env var)
            sandbox: Use sandbox environment (default: True)
        """
        self.access_token = access_token or os.getenv("ZENODO_TOKEN")
        if not self.access_token:
            raise ValueError(
                "Zenodo access token not provided. "
                "Set ZENODO_TOKEN environment variable or pass access_token parameter."
            )

        # Base URL (sandbox or production)
        if sandbox:
            self.base_url = "https://sandbox.zenodo.org/api"
        else:
            self.base_url = "https://zenodo.org/api"

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        print(f"Initialized ZenodoPublisher (sandbox={sandbox})")

    def create_deposition(self, metadata: dict) -> dict:
        """
        Create a new deposition (draft).

        Args:
            metadata: Deposition metadata

        Returns:
            Response data with deposition ID

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.base_url}/deposit/depositions"

        response = requests.post(
            url,
            headers=self.headers,
            json={"metadata": metadata},
        )
        response.raise_for_status()

        data = response.json()
        print(f"Created deposition: {data['id']}")
        return data

    def upload_file(self, deposition_id: int, file_path: str) -> dict:
        """
        Upload file to deposition.

        Args:
            deposition_id: Deposition ID
            file_path: Path to file to upload

        Returns:
            Response data

        Raises:
            FileNotFoundError: If file doesn't exist
            requests.HTTPError: If API request fails
        """
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        url = f"{self.base_url}/deposit/depositions/{deposition_id}/files"

        with open(file_path_obj, "rb") as f:
            response = requests.post(
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                files={"file": f},
                data={"name": file_path_obj.name},
            )

        response.raise_for_status()

        data = response.json()
        print(f"Uploaded file: {file_path_obj.name}")
        return data

    def publish_deposition(self, deposition_id: int) -> dict:
        """
        Publish deposition (make it public and mint DOI).

        Args:
            deposition_id: Deposition ID

        Returns:
            Response data with DOI

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.base_url}/deposit/depositions/{deposition_id}/actions/publish"

        response = requests.post(
            url,
            headers=self.headers,
        )
        response.raise_for_status()

        data = response.json()
        print(f"Published deposition: {data['doi']}")
        return data

    def create_and_publish(
        self,
        metadata: dict,
        files: list[str],
    ) -> dict:
        """
        Complete workflow: create, upload files, and publish.

        Args:
            metadata: Deposition metadata
            files: List of file paths to upload

        Returns:
            Published deposition data with DOI

        Raises:
            Exception: If any step fails
        """
        try:
            # Step 1: Create deposition
            print("Creating deposition...")
            deposition = self.create_deposition(metadata)
            deposition_id = deposition["id"]

            # Step 2: Upload files
            print(f"Uploading {len(files)} file(s)...")
            for file_path in files:
                self.upload_file(deposition_id, file_path)

            # Step 3: Publish
            print("Publishing deposition...")
            published = self.publish_deposition(deposition_id)

            print("\n" + "=" * 70)
            print("SUCCESS! Publication complete")
            print(f"DOI: {published['doi']}")
            print(f"URL: {published['links']['record_html']}")
            print("=" * 70)

            return published

        except Exception as e:
            print(f"Error during publication: {e}", file=sys.stderr)
            raise


def create_voynich_metadata() -> dict:
    """
    Create metadata for Voynich Morphemic Decryption publication.

    Returns:
        Zenodo metadata dictionary
    """
    return {
        "title": "Voynich Manuscript Morphemic Decryption - Analysis Results",
        "upload_type": "dataset",
        "description": (
            "<p>Comprehensive morphemic analysis results for the Voynich Manuscript. "
            "This dataset contains:</p>"
            "<ul>"
            "<li>Morpheme inventory with frequency analysis</li>"
            "<li>Word decomposition results</li>"
            "<li>Statistical validation (chi-square tests)</li>"
            "<li>Confidence metrics and distribution analysis</li>"
            "</ul>"
            "<p>Generated using advanced computational linguistics methods "
            "and statistical validation.</p>"
        ),
        "creators": [
            {
                "name": "Piesiak, Mateusz",
                "affiliation": "Independent Researcher",
                "orcid": "",  # Add ORCID if available
            }
        ],
        "keywords": [
            "Voynich Manuscript",
            "morphemic analysis",
            "computational linguistics",
            "historical cryptography",
            "manuscript studies",
            "XV century",
        ],
        "notes": (
            "This research applies morphemic decomposition techniques "
            "to the Voynich Manuscript text."
        ),
        "related_identifiers": [
            {
                "identifier": "https://github.com/Mati83mon/voynich-morphemic-decryption",
                "relation": "isSupplementTo",
                "resource_type": "software",
            }
        ],
        "contributors": [],
        "references": [],
        "version": "1.0.0",
        "language": "eng",
        "license": "cc-by-4.0",
        "access_right": "open",
    }


def main():
    """Main execution function."""
    print("=" * 70)
    print("Zenodo Publisher - Voynich Morphemic Decryption")
    print("=" * 70)
    print()

    # Check for access token
    if not os.getenv("ZENODO_TOKEN"):
        print("ERROR: ZENODO_TOKEN environment variable not set", file=sys.stderr)
        print("Please set your Zenodo API token:", file=sys.stderr)
        print("  export ZENODO_TOKEN='your_token_here'", file=sys.stderr)
        sys.exit(1)

    # Determine sandbox mode
    sandbox = os.getenv("ZENODO_SANDBOX", "true").lower() == "true"
    print(f"Mode: {'SANDBOX' if sandbox else 'PRODUCTION'}")
    print()

    # Initialize publisher
    publisher = ZenodoPublisher(sandbox=sandbox)

    # Create metadata
    metadata = create_voynich_metadata()

    # Define files to upload
    output_dir = Path("output")
    files_to_upload = []

    # Check for output files
    potential_files = [
        output_dir / "analysis_results.json",
        output_dir / "morpheme_inventory.csv",
        output_dir / "word_analyses.csv",
        output_dir / "analysis_summary.txt",
    ]

    for file_path in potential_files:
        if file_path.exists():
            files_to_upload.append(str(file_path))

    if not files_to_upload:
        print("WARNING: No output files found to upload", file=sys.stderr)
        print("Please run the analysis first to generate output files.", file=sys.stderr)
        sys.exit(1)

    print(f"Files to upload: {len(files_to_upload)}")
    for f in files_to_upload:
        print(f"  - {f}")
    print()

    # Confirm publication (in production mode)
    if not sandbox:
        response = input("Publish to PRODUCTION Zenodo? This will mint a DOI. (yes/no): ")
        if response.lower() != "yes":
            print("Publication cancelled.")
            sys.exit(0)

    # Publish
    try:
        result = publisher.create_and_publish(metadata, files_to_upload)

        # Save result to file
        result_file = output_dir / "zenodo_publication.json"
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"\nPublication details saved to: {result_file}")

    except Exception as e:
        print(f"\nPublication failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
