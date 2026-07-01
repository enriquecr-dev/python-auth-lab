from auth_lab.foundations.user_data import (
    UserRecord,
    count_users_by_role,
    deactivate_user_by_email,
    find_user_by_email,
    get_active_users,
    get_unique_roles,
    get_user_emails,
)


def build_users() -> list[UserRecord]:
    return [
        {
            "id": 1,
            "name": "Enrique",
            "email": " Enrique@Example.COM ",
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
        {
            "id": 3,
            "name": "Luis",
            "email": "luis@example.com",
            "is_active": False,
            "roles": ["viewer"],
        },
    ]


def test_get_active_users_returns_only_active_users() -> None:
    users = build_users()

    active_users = get_active_users(users)

    assert len(active_users) == 2
    assert active_users[0]["name"] == "Enrique"
    assert active_users[1]["name"] == "Ana"


def test_find_user_by_email_returns_user_when_exists() -> None:
    users = build_users()

    user = find_user_by_email(users, "enrique@example.com")

    assert user is not None
    assert user["name"] == "Enrique"


def test_find_user_by_email_returns_none_when_not_exists() -> None:
    users = build_users()

    user = find_user_by_email(users, "missing@example.com")

    assert user is None


def test_get_user_emails_returns_normalized_emails() -> None:
    users = build_users()

    emails = get_user_emails(users)

    assert emails == [
        "enrique@example.com",
        "ana@example.com",
        "luis@example.com",
    ]


def test_get_unique_roles_returns_roles_without_duplicates() -> None:
    users = build_users()

    roles = get_unique_roles(users)

    assert roles == {"admin", "editor", "viewer"}


def test_count_users_by_role_returns_role_summary() -> None:
    users = build_users()

    role_counts = count_users_by_role(users)

    assert role_counts == {
        "admin": 1,
        "editor": 2,
        "viewer": 1,
    }


def test_deactivate_user_by_email_returns_updated_users() -> None:
    users = build_users()

    updated_users = deactivate_user_by_email(users, "enrique@example.com")

    user = find_user_by_email(updated_users, "enrique@example.com")

    assert user is not None
    assert user["is_active"] is False


def test_deactivate_user_by_email_does_not_modify_other_users() -> None:
    users = build_users()

    updated_users = deactivate_user_by_email(users, "enrique@example.com")

    ana = find_user_by_email(updated_users, "ana@example.com")

    assert ana is not None
    assert ana["is_active"] is True
