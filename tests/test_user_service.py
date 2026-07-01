from auth_lab.foundations.user_data import UserRecord
from auth_lab.foundations.user_service import (
    safe_deactivate_user_by_email,
    safe_find_user_by_email,
    validate_user_record,
    validate_users_collection,
)


def build_users() -> list[UserRecord]:
    return [
        {
            "id": 1,
            "name": "Enrique",
            "email": "enrique@example.com",
            "is_active": True,
            "roles": ["admin", "editor"],
        },
        {
            "id": 2,
            "name": "Ana",
            "email": "ana@example.com",
            "is_active": True,
            "roles": ["editor"],
        },
    ]


def test_validate_user_record_accepts_valid_user() -> None:
    user: UserRecord = {
        "id": 1,
        "name": "Enrique",
        "email": "enrique@example.com",
        "is_active": True,
        "roles": ["admin"],
    }

    errors = validate_user_record(user)

    assert errors == []


def test_validate_user_record_rejects_non_dictionary() -> None:
    errors = validate_user_record("invalid-user")

    assert errors == ["User record must be a dictionary."]


def test_validate_user_record_rejects_boolean_id() -> None:
    user = {
        "id": True,
        "name": "Enrique",
        "email": "enrique@example.com",
        "is_active": True,
        "roles": ["admin"],
    }

    errors = validate_user_record(user)

    assert "User id must be an integer." in errors


def test_validate_user_record_rejects_boolean_email() -> None:
    user = {
        "id": 1,
        "name": "Enrique",
        "email": True,
        "is_active": True,
        "roles": ["admin"],
    }

    errors = validate_user_record(user)

    assert "User email must be a string." in errors


def test_validate_user_record_rejects_invalid_roles() -> None:
    user = {
        "id": 1,
        "name": "Enrique",
        "email": "enrique@example.com",
        "is_active": True,
        "roles": ["admin", ""],
    }

    errors = validate_user_record(user)

    assert "User role at index 1 must be a non-empty string." in errors


def test_validate_users_collection_rejects_non_list() -> None:
    errors = validate_users_collection("invalid-users")

    assert errors == ["Users collection must be a list."]


def test_validate_users_collection_reports_indexed_errors() -> None:
    users = [
        {
            "id": 1,
            "name": "Enrique",
            "email": True,
            "is_active": True,
            "roles": ["admin"],
        }
    ]

    errors = validate_users_collection(users)

    assert errors == ["User at index 0: User email must be a string."]


def test_safe_find_user_by_email_returns_user_when_exists() -> None:
    users = build_users()

    result = safe_find_user_by_email(users, "enrique@example.com")

    assert result.success is True
    assert result.message == "User found."
    assert result.user is not None
    assert result.user["name"] == "Enrique"
    assert result.errors == []


def test_safe_find_user_by_email_rejects_invalid_email_type() -> None:
    users = build_users()

    result = safe_find_user_by_email(users, True)

    assert result.success is False
    assert result.message == "User lookup rejected."
    assert result.errors == ["Email must be a string."]


def test_safe_find_user_by_email_rejects_invalid_user_collection() -> None:
    result = safe_find_user_by_email("invalid-users", "enrique@example.com")

    assert result.success is False
    assert result.message == "User lookup rejected."
    assert result.errors == ["Users collection must be a list."]


def test_safe_find_user_by_email_returns_not_found() -> None:
    users = build_users()

    result = safe_find_user_by_email(users, "missing@example.com")

    assert result.success is False
    assert result.message == "User not found."
    assert result.errors == ["User not found."]
    assert result.user is None


def test_safe_deactivate_user_by_email_returns_updated_users() -> None:
    users = build_users()

    result = safe_deactivate_user_by_email(users, "enrique@example.com")

    assert result.success is True
    assert result.message == "User deactivated."
    assert result.errors == []

    deactivated_user = result.users[0]

    assert deactivated_user["email"] == "enrique@example.com"
    assert deactivated_user["is_active"] is False


def test_safe_deactivate_user_by_email_rejects_missing_user() -> None:
    users = build_users()

    result = safe_deactivate_user_by_email(users, "missing@example.com")

    assert result.success is False
    assert result.message == "User deactivation rejected."
    assert result.errors == ["User not found."]
