"""
agents/quality_agent.py

QualityAgent orchestrates all quality metric functions and returns a
structured quality report compatible with the existing agent architecture.
"""

from __future__ import annotations

import pandas as pd
from typing import Any

from utils.quality_metrics import (
    score_missing_values,
    score_duplicates,
    score_constant_columns,
    score_high_cardinality,
    score_outliers,
    score_datatype_consistency,
    score_empty_columns,
    compute_overall_score,
    WEIGHTS,
)


class QualityAgent:

    def analyze(self, df: pd.DataFrame) -> dict[str, Any]:
        """
        Run all quality checks against *df* and return a structured report.

        Parameters:
            df (pd.DataFrame): The dataset to evaluate.

        Returns:
            dict with keys:
                overall_score  – int 0-100
                grade          – str ("Excellent" / "Good" / "Fair" / "Poor")
                metrics        – dict of per-metric scores (int 0-100)
                details        – dict of per-metric raw detail dicts
                warnings       – list[str]
                recommendations – list[str]
                weights        – dict showing the weight of each metric
        """
        # ------------------------------------------------------------------
        # Guard: empty / degenerate DataFrames
        # ------------------------------------------------------------------
        if df is None or df.empty:
            return self._empty_result()

        # ------------------------------------------------------------------
        # Run each metric
        # ------------------------------------------------------------------
        missing_result   = score_missing_values(df)
        dup_result       = score_duplicates(df)
        const_result     = score_constant_columns(df)
        card_result      = score_high_cardinality(df)
        outlier_result   = score_outliers(df)
        dtype_result     = score_datatype_consistency(df)
        empty_result     = score_empty_columns(df)

        # ------------------------------------------------------------------
        # Aggregate metric scores
        # ------------------------------------------------------------------
        metric_scores: dict[str, int] = {
            "missing_values":       missing_result["score"],
            "duplicates":           dup_result["score"],
            "constant_columns":     const_result["score"],
            "high_cardinality":     card_result["score"],
            "outliers":             outlier_result["score"],
            "datatype_consistency": dtype_result["score"],
            "empty_columns":        empty_result["score"],
        }

        overall = compute_overall_score(metric_scores)

        # ------------------------------------------------------------------
        # Warnings
        # ------------------------------------------------------------------
        warnings: list[str] = []

        if missing_result["pct"] > 0:
            warnings.append(
                f"{missing_result['pct']:.1f}% of all cells contain missing values "
                f"({len(missing_result['per_column'])} column(s) affected)."
            )

        if dup_result["count"] > 0:
            warnings.append(
                f"{dup_result['count']} duplicate row(s) found "
                f"({dup_result['pct']:.1f}% of the dataset)."
            )

        if const_result["columns"]:
            warnings.append(
                f"Constant column(s) detected (single unique value): "
                f"{', '.join(const_result['columns'])}."
            )

        if card_result["columns"]:
            warnings.append(
                f"High-cardinality column(s) detected (≥90% unique values): "
                f"{', '.join(card_result['columns'])}."
            )

        if outlier_result["pct_rows"] > 0:
            warnings.append(
                f"{outlier_result['pct_rows']:.1f}% of rows contain at least one numeric outlier."
            )

        if dtype_result["numeric_as_object"]:
            warnings.append(
                f"Column(s) stored as text but contain numeric data: "
                f"{', '.join(dtype_result['numeric_as_object'])}."
            )

        if dtype_result["mixed_type_columns"]:
            warnings.append(
                f"Column(s) with mixed data types detected: "
                f"{', '.join(dtype_result['mixed_type_columns'])}."
            )

        if empty_result["columns"]:
            warnings.append(
                f"Completely empty column(s) detected: "
                f"{', '.join(empty_result['columns'])}."
            )

        # ------------------------------------------------------------------
        # Recommendations
        # ------------------------------------------------------------------
        recommendations: list[str] = []

        if missing_result["pct"] > 5:
            recommendations.append(
                "Impute or remove columns / rows with high missing-value rates "
                "before modelling."
            )
        elif missing_result["pct"] > 0:
            recommendations.append(
                "Fill the remaining missing values using median (numeric) or "
                "mode (categorical) imputation."
            )

        if dup_result["count"] > 0:
            recommendations.append(
                "Drop duplicate rows with df.drop_duplicates() to avoid "
                "skewed statistics and overfitting."
            )

        if const_result["columns"]:
            recommendations.append(
                f"Drop constant column(s) {const_result['columns']} — they carry "
                "no information and will not help any model."
            )

        if card_result["columns"]:
            recommendations.append(
                f"Consider hashing, binning, or dropping the high-cardinality "
                f"column(s) {card_result['columns']} to reduce noise."
            )

        if outlier_result["pct_rows"] > 10:
            recommendations.append(
                "More than 10% of rows contain outliers. Investigate whether "
                "they are data-entry errors or genuine extreme values, then "
                "cap, transform, or remove them as appropriate."
            )
        elif outlier_result["pct_rows"] > 0:
            recommendations.append(
                "Review the flagged outlier rows and apply winsorisation or "
                "log-transformation if needed."
            )

        if dtype_result["numeric_as_object"]:
            recommendations.append(
                f"Cast {dtype_result['numeric_as_object']} to a numeric dtype "
                "with pd.to_numeric() to unlock numeric operations."
            )

        if dtype_result["mixed_type_columns"]:
            recommendations.append(
                f"Standardise the mixed-type column(s) "
                f"{dtype_result['mixed_type_columns']} to a single dtype."
            )

        if empty_result["columns"]:
            recommendations.append(
                f"Remove completely empty column(s) {empty_result['columns']} "
                "as they provide no usable information."
            )

        if not recommendations:
            recommendations.append(
                "No major data quality issues detected. The dataset looks clean "
                "and ready for analysis."
            )

        # ------------------------------------------------------------------
        # Assemble result
        # ------------------------------------------------------------------
        return {
            "overall_score": overall,
            "grade": _grade(overall),
            "metrics": metric_scores,
            "details": {
                "missing_values":       missing_result,
                "duplicates":           dup_result,
                "constant_columns":     const_result,
                "high_cardinality":     card_result,
                "outliers":             outlier_result,
                "datatype_consistency": dtype_result,
                "empty_columns":        empty_result,
            },
            "warnings":        warnings,
            "recommendations": recommendations,
            "weights":         WEIGHTS,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _empty_result() -> dict[str, Any]:
        return {
            "overall_score": 0,
            "grade": "Poor",
            "metrics": {},
            "details": {},
            "warnings": ["The dataset is empty — no quality metrics could be computed."],
            "recommendations": ["Load a non-empty dataset to receive quality recommendations."],
            "weights": WEIGHTS,
        }


# ------------------------------------------------------------------
# Module-level helper (also used by dashboard for colour coding)
# ------------------------------------------------------------------

def _grade(score: int) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 60:
        return "Fair"
    return "Poor"
