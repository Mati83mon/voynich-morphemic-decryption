"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from voynich_decryption.api.app import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint returns health info."""
        response = client.get("/api/v1/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "version" in data

    def test_health_check_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestAnalysisEndpoints:
    """Test analysis endpoints."""

    def test_analyze_vocabulary_endpoint(self):
        """Test vocabulary analysis endpoint."""
        request_data = {
            "vocabulary": {
                "word_001": "qodyain",
                "word_002": "qokeedy",
                "word_003": "dain",
            }
        }

        response = client.post("/api/v1/analyze", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "analysis_id" in data
        assert data["total_words_analyzed"] == 3

    def test_analyze_vocabulary_empty_raises_error(self):
        """Test analyzing empty vocabulary returns error."""
        request_data = {"vocabulary": {}}

        response = client.post("/api/v1/analyze", json=request_data)

        assert response.status_code == 500  # Internal error for now

    def test_analyze_detailed_endpoint(self):
        """Test detailed analysis endpoint."""
        request_data = {
            "vocabulary": {
                "word_001": "qodyain",
                "word_002": "qokeedy",
            }
        }

        response = client.post("/api/v1/analyze/detailed", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "morpheme_inventory" in data
        assert "word_analyses" in data


class TestDecompositionEndpoint:
    """Test word decomposition endpoint."""

    def test_decompose_word_endpoint(self):
        """Test word decomposition endpoint."""
        request_data = {
            "word": "qodyain",
            "word_id": "test_001",
        }

        response = client.post("/api/v1/decompose", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["word"] == "qodyain"
        assert data["word_id"] == "test_001"
        assert "morphemes" in data

    def test_decompose_word_without_id(self):
        """Test decomposing word without providing ID."""
        request_data = {"word": "qo"}

        response = client.post("/api/v1/decompose", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "word_id" in data  # Should be auto-generated


class TestUtilityEndpoints:
    """Test utility endpoints."""

    def test_get_statistics_endpoint(self):
        """Test getting analyzer statistics."""
        response = client.get("/api/v1/statistics")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_clear_cache_endpoint(self):
        """Test clearing analyzer cache."""
        response = client.post("/api/v1/cache/clear")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
