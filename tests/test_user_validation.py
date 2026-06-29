from auth_lab.foundations.user_validation import (
    is_strong_password,
    is_valid_email,
    normalize_email,
    validate_registration_data,
)


def test_normalize_email_removes_spaces_and_lowercases_text() -> None:
    email = " Enrique@Example.COM "

    result = normalize_email(email)

    assert result == "enrique@example.com"


def test_valid_email_returns_true() -> None:
    assert is_valid_email("enrique@example.com") is True


def test_email_without_at_returns_false() -> None:
    assert is_valid_email("enriqueexample.com") is False


def test_email_with_two_at_symbols_returns_false() -> None:
    assert is_valid_email("enrique@@example.com") is False


def test_email_without_domain_dot_returns_false() -> None:
    assert is_valid_email("enrique@example") is False


def test_strong_password_returns_true() -> None:
    assert is_strong_password("Password123!") is True


def test_weak_password_returns_false() -> None:
    assert is_strong_password("password") is False


def test_valid_registration_data_returns_empty_error_list() -> None:
    errors = validate_registration_data(
        name="Enrique",
        email="enrique@example.com",
        password="Password123!",
    )

    assert errors == []


def test_invalid_registration_data_returns_errors() -> None:
    errors = validate_registration_data(
        name="",
        email="invalid-email",
        password="123",
    )

    assert len(errors) == 3
