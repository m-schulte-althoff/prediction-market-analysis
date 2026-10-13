"""Tests for auditable literal rule-text measurement."""

import math

import pandas as pd
import pytest

from src.semantics import add_semantic_features, pair_divergence, semantic_features


def test_clock_context_recognizes_et_without_mistaking_et_al_for_timezone() -> None:
    """Common platform deadline notation earns the same credit as EDT."""

    question = "Will the deal be signed by June 30, 2026?"
    eastern = semantic_features(question, "Deadline: 11:59 PM ET.")
    daylight = semantic_features(question, "Deadline: 11:59 PM EDT.")
    no_zone = semantic_features(question, "Deadline: 11:59 PM, according to Smith et al.")
    assert eastern["temporal_specificity"] == daylight["temporal_specificity"]
    assert eastern["temporal_specificity"] > no_zone["temporal_specificity"]


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


@pytest.mark.parametrize("quote", ['"Yes"', "'YES'", "“Yes”", "‘Yes’"])
def test_quoted_yes_preserves_definition_credit(quote: str) -> None:
    """Harmless quote punctuation and phrase spacing preserve definition credit."""

    quoted = semantic_features("Result", f"This market resolves  to {quote}   if Alice wins.")
    unquoted = semantic_features("Result", "This market resolves to Yes if Alice wins.")
    assert quoted["outcome_definition"] == unquoted["outcome_definition"]
    no_if = semantic_features("Result", f"A proposal resolves to {quote}.")
    assert no_if["outcome_definition"] < quoted["outcome_definition"]


@pytest.mark.parametrize("threshold", ["5%", "5%.", "5 %.", "5 percent."])
def test_percent_unit_credit_is_insensitive_to_formatting(threshold: str) -> None:
    """A percent threshold remains recognized at punctuation and end of text."""

    measured = semantic_features("Result", f"The threshold is {threshold}")
    assert measured["quantitative_threshold"] == 1.0
    assert semantic_features("Result", "There were 5 participants.")["quantitative_threshold"] == 0


def test_tie_tokens_and_intended_stems_have_distinct_controls() -> None:
    """Unrelated substrings lose tie credit while real tokens and other stems remain."""

    unrelated = semantic_features("Result", "The parties and committees report.")
    assert unrelated["edge_completeness"] == 0
    for word in ("tie", "ties", "tied", "postponement", "cancellation", "inauguration"):
        assert semantic_features("Result", f"A {word} is recorded.")["edge_completeness"] == 0.12


def test_threshold_and_clock_language_do_not_share_deadline_credit() -> None:
    """At least is quantitative language; at a detected time receives clock credit."""

    threshold = semantic_features("Result", "At least 5 votes are required.")
    assert threshold["temporal_specificity"] == 0.0
    assert threshold["quantitative_threshold"] == 1.0
    assert semantic_features("Result", "At 5 pm.")["temporal_specificity"] == 0.30
    assert semantic_features("Result", "The habitat is established.")["temporal_specificity"] == 0


def test_repeated_named_authority_does_not_depend_on_field_placement() -> None:
    """Identical authority information receives the same component weights across fields."""

    direct = semantic_features("Result", "Reuters")
    moved = semantic_features("Result", "", "Reuters")
    repeated = semantic_features("Result", "Reuters", "Reuters")
    assert direct["source_specificity"] == moved["source_specificity"] == 1.0
    assert direct["source_specificity"] == repeated["source_specificity"]
    assert direct["determinacy_score"] == repeated["determinacy_score"]


def test_missing_rules_do_not_mean_no_discretion() -> None:
    """An absent rule field remains unknown even when a source or question is present."""

    absent = semantic_features("Will Alice win?", "", "Reuters")
    present = semantic_features("Will Alice win?", "Alice must win.", "Reuters")
    assert absent["rule_text_missing"] == 1.0
    assert math.isnan(absent["discretion_clarity"])
    assert math.isnan(absent["determinacy_score"])
    assert present["discretion_clarity"] == 1.0
    frame = pd.DataFrame(
        [{"question": "Will Alice win?", "rules": None, "resolution_source": None}]
    )
    measured = add_semantic_features(frame)
    assert measured.loc[0, "rule_text_missing"] == 1
    assert measured.loc[0, "rule_word_count"] == 3
