"""Tests for auditable semantic measurement."""

from src.semantics import pair_divergence, semantic_features


def test_specific_rule_scores_above_ambiguous_rule() -> None:
    """A named source, deadline, threshold, and fallback increase determinacy."""

    specific = semantic_features(
        "Will CPI exceed 3.0% in January 2026?",
        (
            "Resolves Yes if CPI is greater than 3.0% according to the Bureau of Labor "
            "Statistics release at 8:30 a.m. EST on February 13, 2026. If the release is "
            "revised, the first published value governs; otherwise the market resolves No."
        ),
        "Bureau of Labor Statistics",
    )
    ambiguous = semantic_features(
        "Will there be a significant deal?",
        "Resolves using a consensus of credible reporting.",
    )

    assert specific["determinacy_score"] > ambiguous["determinacy_score"]
    assert specific["source_specificity"] == 1.0
    assert specific["temporal_specificity"] == 1.0
    assert specific["edge_completeness"] > ambiguous["edge_completeness"]


def test_year_is_not_misclassified_as_quantitative_threshold() -> None:
    """Calendar years are time boundaries, not substantive numeric predicates."""

    temporal = semantic_features(
        "Will the candidate win in 2028?",
        "Resolves Yes if the candidate wins the 2028 election.",
    )
    threshold = semantic_features(
        "Will inflation exceed 3%?",
        "Resolves Yes if inflation is greater than 3 percent.",
    )

    assert temporal["numeric_mention"] == 1.0
    assert temporal["quantitative_threshold"] == 0.0
    assert threshold["quantitative_threshold"] == 1.0


def test_pair_divergence_is_zero_for_identical_structured_conditions() -> None:
    """Identical wording and conditions have zero measured divergence."""

    text = "Resolves according to Reuters if signed by January 20, 2026."
    result = pair_divergence(text, text, lexical_similarity=1.0, deadline_days=0.0)

    assert result["semantic_divergence"] == 0.0
    assert result["identified_semantic_difference"] == "no structured difference detected"


def test_stage_difference_is_distinct_from_wording() -> None:
    """Announcement and implementation are recognized as different event stages."""

    result = pair_divergence(
        "A deal is announced by January 20, 2026.",
        "A deal is implemented by January 20, 2026.",
        lexical_similarity=0.8,
        deadline_days=0.0,
    )

    assert result["stage_divergence"] == 1.0
    assert "required event stage differs" in str(result["identified_semantic_difference"])


def test_announcement_qualification_difference_is_human_readable() -> None:
    """Opposed departure triggers produce a concrete diagnostic, not only a score."""

    result = pair_divergence(
        "An announcement that the president will leave is encompassed and resolves to Yes.",
        "An announcement of resignation will not alone qualify; permanent removal is required.",
        lexical_similarity=0.7,
        deadline_days=0.0,
    )

    assert "announcement can qualify on Kalshi" in str(result["identified_semantic_difference"])
