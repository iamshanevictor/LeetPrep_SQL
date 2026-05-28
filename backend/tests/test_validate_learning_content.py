from scripts.validate_learning_content import validate_learning_content


def test_learning_content_validation_passes():
    assert validate_learning_content() == []
