"""
utils/quality_metrics.py

Low-level metric functions for the Data Quality Score feature.
Each function accepts a pandas DataFrame and returns a score (0–100)
plus any associated detail needed by the QualityAgent.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Any


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_divide(numerator: float, denominator: float, fallback: float = 0.0) -> float:
    """Return numerator / denominator, or fallback when denominator is zero."""
    return numerator / denominator if denominator else fallback


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    """Clamp a value to [lo, hi]."""
    return max(lo, min(hi, value))


# ---------------------------------------------------------------------------
# 1. Missing Values
# ---------------------------------------------------------------------------

def score_missing_values(df: pd.DataFrame) -> dict[str, Any]:
    """
    Score based on the percentage of missing (NaN) cells across the whole dataset.

    Penalty curve:
        0 %  missing  → 100
        100% missing  →   0
    Uses a linear decay so every percentage point costs 1 point.

    Returns:
        score      – int 0-100
        pct        – float, overall missing-value percentage
        per_column – dict {col: missing_count}
    """
    if df.empty or df.size == 0:
        return {"score": 100, "pct": 0.0, "per_column": {}}

    total_cells = df.size
    missing_cells = int(df.isnull().sum().sum())
    pct = _safe_divide(missing_cells * 100.0, total_cells)

    score = _clamp(100.0 - pct)

    per_column = {
        col: int(count)
        for col, count in df.isnull().sum().items()
        if count > 0
    }

    return {
        "score": round(score),
        "pct": round(pct, 2),
        "per_column": per_column,
    }


# ---------------------------------------------------------------------------
# 2. Duplicate Rows
# ---------------------------------------------------------------------------

def score_duplicates(df: pd.DataFrame) -> dict[str, Any]:
    """
    Score based on the percentage of duplicate rows.

    Penalty: linear, 0 % duplicates → 100, 100 % → 0.

    Returns:
        score – int 0-100
        count – int, number of duplicate rows
        pct   – float
    """
    if df.empty or len(df) == 0:
        return {"score": 100, "count": 0, "pct": 0.0}

    count = int(df.duplicated().sum())
    pct = _safe_divide(count * 100.0, len(df))
    score = _clamp(100.0 - pct)

    return {
        "score": round(score),
        "count": count,
        "pct": round(pct, 2),
    }


# ---------------------------------------------------------------------------
# 3. Constant Columns
# ---------------------------------------------------------------------------

def score_constant_columns(df: pd.DataFrame) -> dict[str, Any]:
    """
    Penalise columns that contain only a single unique (non-null) value.
    Each constant column removes (100 / total_columns) points, floored at 0.

    Returns:
        score   – int 0-100
        columns – list of constant column names
    """
    if df.empty or df.shape[1] == 0:
        return {"score": 100, "columns": []}

    constant_cols = [
        col for col in df.columns
        if df[col].dropna().nunique() <= 1
    ]

    penalty_per_col = _safe_divide(100.0, df.shape[1])
    score = _clamp(100.0 - len(constant_cols) * penalty_per_col)

    return {
        "score": round(score),
        "columns": constant_cols,
    }


# ---------------------------------------------------------------------------
# 4. High-Cardinality Columns
# ---------------------------------------------------------------------------

def score_high_cardinality(df: pd.DataFrame, threshold: float = 0.9) -> dict[str, Any]:
    """
    Flag categorical (object/string) columns whose ratio of unique values to
    total rows exceeds `threshold`.  These are often ID-like columns that add
    little analytical value and can mislead models.

    Scoring: each flagged column subtracts (100 / total_object_cols) points.
    If there are no object columns the score is 100 (not applicable).

    Returns:
        score   – int 0-100
        columns – list of high-cardinality column names
    """
    object_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if not object_cols or len(df) == 0:
        return {"score": 100, "columns": []}

    high_card_cols = []
    for col in object_cols:
        ratio = _safe_divide(df[col].nunique(), len(df))
        if ratio >= threshold:
            high_card_cols.append(col)

    penalty_per_col = _safe_divide(100.0, len(object_cols))
    score = _clamp(100.0 - len(high_card_cols) * penalty_per_col)

    return {
        "score": round(score),
        "columns": high_card_cols,
    }


# ---------------------------------------------------------------------------
# 5. Numeric Outliers  (IQR method)
# ---------------------------------------------------------------------------

def score_outliers(df: pd.DataFrame) -> dict[str, Any]:
    """
    Detect outliers in every numeric column using the IQR fences
    (Q1 - 1.5·IQR, Q3 + 1.5·IQR).  Score is based on the fraction of
    *rows* that contain at least one outlier value.

    Penalty: linear, 0 % outlier-rows → 100, 100 % → 0.

    Returns:
        score        – int 0-100
        pct_rows     – float, percentage of rows with ≥1 outlier
        per_column   – dict {col: outlier_count}
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols or len(df) == 0:
        return {"score": 100, "pct_rows": 0.0, "per_column": {}}

    outlier_mask = pd.Series(False, index=df.index)
    per_column: dict[str, int] = {}

    for col in numeric_cols:
        series = df[col].dropna()
        if series.empty:
            per_column[col] = 0
            continue

        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr

        col_mask = (df[col] < lower) | (df[col] > upper)
        per_column[col] = int(col_mask.sum())
        outlier_mask = outlier_mask | col_mask

    outlier_rows = int(outlier_mask.sum())
    pct_rows = _safe_divide(outlier_rows * 100.0, len(df))
    score = _clamp(100.0 - pct_rows)

    return {
        "score": round(score),
        "pct_rows": round(pct_rows, 2),
        "per_column": per_column,
    }


# ---------------------------------------------------------------------------
# 6. Data-Type Consistency
# ---------------------------------------------------------------------------

def score_datatype_consistency(df: pd.DataFrame) -> dict[str, Any]:
    """
    Detect two types of type issues:
      a) Object columns that are actually numeric (coercible with pd.to_numeric).
      b) Columns with mixed Python types within the same object column (excluding NaN).

    Each problematic column removes (100 / total_columns) points.

    Returns:
        score              – int 0-100
        numeric_as_object  – list of cols that look numeric but are stored as object
        mixed_type_columns – list of cols with mixed Python types
    """
    if df.empty or df.shape[1] == 0:
        return {
            "score": 100,
            "numeric_as_object": [],
            "mixed_type_columns": [],
        }

    object_cols = df.select_dtypes(include=["object"]).columns.tolist()
    numeric_as_object: list[str] = []
    mixed_type_cols: list[str] = []

    for col in object_cols:
        non_null = df[col].dropna()
        if non_null.empty:
            continue

        # Check if it looks numeric
        converted = pd.to_numeric(non_null, errors="coerce")
        if converted.notna().all():
            numeric_as_object.append(col)
            continue  # already classified; skip mixed-type check

        # Check for mixed Python types
        unique_types = set(type(v) for v in non_null)
        if len(unique_types) > 1:
            mixed_type_cols.append(col)

    total_cols = df.shape[1]
    bad_cols = len(set(numeric_as_object + mixed_type_cols))
    penalty_per_col = _safe_divide(100.0, total_cols)
    score = _clamp(100.0 - bad_cols * penalty_per_col)

    return {
        "score": round(score),
        "numeric_as_object": numeric_as_object,
        "mixed_type_columns": mixed_type_cols,
    }


# ---------------------------------------------------------------------------
# 7. Empty Columns
# ---------------------------------------------------------------------------

def score_empty_columns(df: pd.DataFrame) -> dict[str, Any]:
    """
    Detect columns that are entirely empty (all values are NaN).
    Each empty column removes (100 / total_columns) points.

    Returns:
        score   – int 0-100
        columns – list of completely empty column names
    """
    if df.empty or df.shape[1] == 0:
        return {"score": 100, "columns": []}

    empty_cols = [col for col in df.columns if df[col].isnull().all()]
    penalty_per_col = _safe_divide(100.0, df.shape[1])
    score = _clamp(100.0 - len(empty_cols) * penalty_per_col)

    return {
        "score": round(score),
        "columns": empty_cols,
    }


# ---------------------------------------------------------------------------
# Weighted overall score
# ---------------------------------------------------------------------------

WEIGHTS: dict[str, float] = {
    "missing_values":       0.30,
    "duplicates":           0.20,
    "outliers":             0.15,
    "constant_columns":     0.10,
    "datatype_consistency": 0.15,
    "empty_columns":        0.10,
}


def compute_overall_score(metric_scores: dict[str, int]) -> int:
    """
    Combine individual metric scores into a single weighted overall score.

    Parameters:
        metric_scores – dict mapping metric name → score (0-100)

    Returns:
        overall score clamped to [0, 100]
    """
    total = sum(
        WEIGHTS.get(key, 0.0) * score
        for key, score in metric_scores.items()
    )
    return round(_clamp(total))
