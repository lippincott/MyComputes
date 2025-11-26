# report_matching.py
import re
from difflib import SequenceMatcher


def _normalize_text(value: str) -> str:
    """
    Normalize text for comparison:
    - Handle None
    - Lowercase
    - Collapse whitespace
    """
    if not value:
        return ""
    value = value.strip().lower()
    # collapse multiple spaces/newlines/tabs to single space
    value = re.sub(r"\s+", " ", value)
    return value


def text_match_score(user_text: str, ai_text: str):
    """
    Return (score, note) where score is 0–100 based on similarity.
    Ignores case/whitespace differences but calls them out in the note.
    """
    u = _normalize_text(user_text)
    a = _normalize_text(ai_text)

    # Both empty
    if not u and not a:
        return 100.0, "Both user and AI values are empty."

    # One side missing
    if not u or not a:
        return 0.0, "Value present on only one side (user vs AI)."

    ratio = SequenceMatcher(None, u, a).ratio() * 100.0
    score = round(ratio, 1)

    if u == a:
        note = "Exact match (ignoring case/whitespace)."
    elif score >= 90:
        note = "Very close match; minor differences (e.g., punctuation, capitalization)."
    elif score >= 70:
        note = "Partial match; wording or extra words differ."
    else:
        note = "Low similarity; likely different values."

    return score, note


def numeric_match_score(user_value, ai_value, tolerance=0.1):
    """
    Return (score, note) for numeric fields (ABV, volumes).
    - 100 if same within tolerance.
    - Otherwise score decreases with relative difference.
    """
    if user_value is None and ai_value is None:
        return 100.0, "Both user and AI values are empty."
    if user_value is None or ai_value is None:
        return 0.0, "Value present on only one side (user vs AI)."

    try:
        u = float(user_value)
        a = float(ai_value)
    except (TypeError, ValueError):
        return 0.0, "Could not parse numeric value on one or both sides."

    diff = abs(u - a)

    if diff <= tolerance:
        return 100.0, f"Exact match within ±{tolerance}."

    base = max(abs(u), abs(a), 1e-6)
    rel = diff / base  # relative difference (0.0–∞)
    score = max(0.0, 100.0 * (1.0 - rel))  # linear penalty
    score = round(score, 1)
    note = f"Difference of {diff:.2f} ({rel:.1%} relative difference)."
    return score, note


def bool_match_score(user_value, ai_value):
    """
    100 if same boolean, else 0. Handles None as 'missing'.
    """
    if user_value is None and ai_value is None:
        return 100.0, "Both user and AI values are empty."
    if user_value is None or ai_value is None:
        return 0.0, "Value present on only one side (user vs AI)."

    if bool(user_value) == bool(ai_value):
        return 100.0, "Exact match."
    return 0.0, "User and AI values differ."



def apply_match_scores(report):
    """
    Mutates the report instance in-place, filling match_* and note_* fields.
    """

    # Text fields
    report.match_brand, report.note_brand = text_match_score(
        report.brand, report.ai_brand
    )
    report.match_product_name, report.note_product_name = text_match_score(
        report.product_name, report.ai_product_name
    )
    report.match_product_type, report.note_product_type = text_match_score(
        report.product_type, report.ai_product_type
    )
    report.match_warning_text, report.note_warning_text = text_match_score(
        report.warning_text, report.ai_warning_text
    )

    # Numeric fields
    report.match_abv, report.note_abv = numeric_match_score(
        report.abv, report.ai_abv, tolerance=0.1
    )
    report.match_milliliters, report.note_milliliters = numeric_match_score(
        report.milliliters, report.ai_milliliters, tolerance=1.0
    )
    report.match_fl_oz, report.note_fl_oz = numeric_match_score(
        report.fl_oz, report.ai_fl_oz, tolerance=0.1
    )

    # Booleans
    report.match_warning_label, report.note_warning_label = bool_match_score(
        report.warning_label, report.ai_warning_label
    )
