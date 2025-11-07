"""Pydantic schemas for FastAPI endpoints."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MorphemeSchema(BaseModel):
    """Schema for morpheme data."""

    model_config = ConfigDict(from_attributes=True)

    morpheme_id: str = Field(..., description="Unique identifier for the morpheme")
    glyph: str = Field(..., description="The morpheme glyph/text")
    type: str = Field(..., description="Morpheme type (root, prefix, suffix, etc.)")
    frequency: int = Field(0, ge=0, description="Occurrence frequency")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confidence score")
    botanical_reference: str | None = Field(None, description="Botanical context reference")
    pharmaceutical_use: str | None = Field(None, description="Pharmaceutical context")


class WordAnalysisSchema(BaseModel):
    """Schema for word analysis results."""

    model_config = ConfigDict(from_attributes=True)

    word_id: str = Field(..., description="Unique word identifier")
    word_glyph: str = Field(..., description="The word glyph/text")
    morpheme_count: int = Field(0, ge=0, description="Number of morphemes")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Overall confidence")
    verification_status: str = Field("unverified", description="Verification status")
    morphemes: list[MorphemeSchema] = Field(
        default_factory=list, description="List of identified morphemes"
    )


class AnalysisRequest(BaseModel):
    """Schema for analysis request."""

    vocabulary: dict[str, str] = Field(
        ..., description="Dictionary of word_id -> word_glyph to analyze"
    )
    morpheme_inventory: dict[str, dict] | None = Field(
        None, description="Optional predefined morpheme inventory"
    )
    significance_threshold: float = Field(
        0.05,
        ge=0.0,
        le=1.0,
        description="Statistical significance threshold (default: 0.05)",
    )


class AnalysisResponse(BaseModel):
    """Schema for analysis response."""

    model_config = ConfigDict(from_attributes=True)

    success: bool = Field(..., description="Whether analysis succeeded")
    message: str = Field(..., description="Status message")
    analysis_id: str = Field(..., description="Unique analysis identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    total_words_analyzed: int = Field(0, ge=0, description="Total words analyzed")
    total_unique_words: int = Field(0, ge=0, description="Unique word count")
    morphemes_identified: int = Field(0, ge=0, description="Morphemes identified")
    chi_square_statistic: float = Field(0.0, description="Chi-square test statistic")
    p_value: float = Field(1.0, ge=0.0, le=1.0, description="Statistical p-value")
    statistically_significant: bool = Field(
        False, description="Whether results are statistically significant"
    )
    average_confidence: float = Field(0.0, ge=0.0, le=1.0, description="Average word confidence")


class AnalysisDetailResponse(AnalysisResponse):
    """Detailed analysis response with full results."""

    morpheme_inventory: dict[str, MorphemeSchema] = Field(
        default_factory=dict, description="Complete morpheme inventory"
    )
    word_analyses: list[WordAnalysisSchema] = Field(
        default_factory=list, description="All word analysis results"
    )
    validation_results: dict | None = Field(None, description="Statistical validation results")


class WordDecompositionRequest(BaseModel):
    """Schema for single word decomposition request."""

    word: str = Field(..., min_length=1, description="Word to decompose")
    word_id: str | None = Field(None, description="Optional word identifier")


class WordDecompositionResponse(BaseModel):
    """Schema for word decomposition response."""

    success: bool = Field(..., description="Whether decomposition succeeded")
    word: str = Field(..., description="The analyzed word")
    word_id: str = Field(..., description="Word identifier")
    morphemes: list[MorphemeSchema] = Field(
        default_factory=list, description="Identified morphemes"
    )
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Overall confidence")
    morpheme_count: int = Field(0, ge=0, description="Number of morphemes")


class HealthResponse(BaseModel):
    """Schema for health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    error: bool = Field(True, description="Error flag")
    message: str = Field(..., description="Error message")
    detail: str | None = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
