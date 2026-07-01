from typing import TypedDict

from auth_lab.foundations.user_validation import normalize_email


class UserRecord(TypedDict):
    id: int
    name: str
    email: str
    is_active: bool
    roles: list[str]


def get_active_users(users: list[UserRecord]) -> list[UserRecord]:
    active_users: list[UserRecord] = []

    for user in users:
        if user["is_active"]:
            active_users.append(user)

    return active_users


def find_user_by_email(users: list[UserRecord], email: str) -> UserRecord | None:
    normalized_email = normalize_email(email)

    for user in users:
        if normalize_email(user["email"]) == normalized_email:
            return user

    return None


def get_user_emails(users: list[UserRecord]) -> list[str]:
    emails: list[str] = []

    for user in users:
        emails.append(normalize_email(user["email"]))

    return emails


def get_unique_roles(users: list[UserRecord]) -> set[str]:
    unique_roles: set[str] = set()

    for user in users:
        for role in user["roles"]:
            unique_roles.add(role)

    return unique_roles


def count_users_by_role(users: list[UserRecord]) -> dict[str, int]:
    role_counts: dict[str, int] = {}

    for user in users:
        for role in user["roles"]:
            if role not in role_counts:
                role_counts[role] = 0

            role_counts[role] += 1

    return role_counts


def deactivate_user_by_email(
    users: list[UserRecord],
    email: str,
) -> list[UserRecord]:
    normalized_email = normalize_email(email)
    updated_users: list[UserRecord] = []

    for user in users:
        if normalize_email(user["email"]) == normalized_email:
            updated_user: UserRecord = {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "is_active": False,
                "roles": list(user["roles"]),
            }

            updated_users.append(updated_user)
            continue

        updated_users.append(user)

    return updated_users
