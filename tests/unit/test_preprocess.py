from app.ingestion.preprocess import clean_text


def test_clean_text_collapses_spaces_and_blank_lines() -> None:
    raw = "Policy   text\n\n\n\nWith\tspaces"
    assert clean_text(raw) == "Policy text\n\nWith spaces"
