"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from voynich_decryption.api.app import app


@pytest.fixture
def client():
    """Create test client fixture."""
    with TestClient(app) as test_client:
        yield test_client


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns health info."""
        response = client.get("/api/v1/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "version" in data

    def test_health_check_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestAnalysisEndpoints:
    """Test analysis endpoints."""

    def test_analyze_vocabulary_endpoint(self, client):
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

    def test_analyze_vocabulary_empty_raises_error(self, client):
        """Test analyzing empty vocabulary returns error."""
        request_data = {"vocabulary": {}}

        response = client.post("/api/v1/analyze", json=request_data)

        assert response.status_code == 400  # Bad Request for invalid input

    def test_analyze_detailed_endpoint(self, client):
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

    def test_decompose_word_endpoint(self, client):
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

    def test_decompose_word_without_id(self, client):
        """Test decomposing word without providing ID."""
        request_data = {"word": "qo"}

        response = client.post("/api/v1/decompose", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "word_id" in data  # Should be auto-generated


class TestUtilityEndpoints:
    """Test utility endpoints."""

    def test_get_statistics_endpoint(self, client):
        """Test getting analyzer statistics."""
        response = client.get("/api/v1/statistics")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_clear_cache_endpoint(self, client):
        """Test clearing analyzer cache."""
        response = client.post("/api/v1/cache/clear")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
