from dataclasses import dataclass, field
from typing import cast

from auth_lab.foundations.user_data import (
    UserRecord,
    deactivate_user_by_email,
    find_user_by_email,
)
from auth_lab.foundations.user_validation import is_valid_email


@dataclass(frozen=True)
class UserLookupResult:
    success: bool
    message: str
    user: UserRecord | None = None
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class UserListResult:
    success: bool
    message: str
    users: list[UserRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def validate_user_record(user: object) -> list[str]:
    errors: list[str] = []

    if not isinstance(user, dict):
        return ["User record must be a dictionary."]

    user_id = user.get("id")
    name = user.get("name")
    email = user.get("email")
    is_active = user.get("is_active")
    roles = user.get("roles")

    if not isinstance(user_id, int) or isinstance(user_id, bool):
        errors.append("User id must be an integer.")

    if not isinstance(name, str) or not name.strip():
        errors.append("User name must be a non-empty string.")

    if not isinstance(email, str):
        errors.append("User email must be a string.")
    elif not is_valid_email(email):
        errors.append("User email is not valid.")

    if not isinstance(is_active, bool):
        errors.append("User active status must be a boolean.")

    if not isinstance(roles, list):
        errors.append("User roles must be a list.")
    else:
        for index, role in enumerate(roles):
            if not isinstance(role, str) or not role.strip():
                errors.append(f"User role at index {index} must be a non-empty string.")

    return errors


def validate_users_collection(users: object) -> list[str]:
    errors: list[str] = []

    if not isinstance(users, list):
        return ["Users collection must be a list."]

    for index, user in enumerate(users):
        user_errors = validate_user_record(user)

        for error in user_errors:
            errors.append(f"User at index {index}: {error}")

    return errors


def safe_find_user_by_email(users: object, email: object) -> UserLookupResult:
    errors: list[str] = []

    if not isinstance(email, str):
        errors.append("Email must be a string.")
    elif not is_valid_email(email):
        errors.append("Email is not valid.")

    errors.extend(validate_users_collection(users))

    if errors:
        return UserLookupResult(
            success=False,
            message="User lookup rejected.",
            errors=errors,
        )

    valid_users = cast(list[UserRecord], users)
    valid_email = cast(str, email)

    user = find_user_by_email(valid_users, valid_email)

    if user is None:
        return UserLookupResult(
            success=False,
            message="User not found.",
            errors=["User not found."],
        )

    return UserLookupResult(
        success=True,
        message="User found.",
        user=user,
    )


def safe_deactivate_user_by_email(users: object, email: object) -> UserListResult:
    lookup_result = safe_find_user_by_email(users, email)

    if not lookup_result.success:
        return UserListResult(
            success=False,
            message="User deactivation rejected.",
            errors=lookup_result.errors,
        )

    valid_users = cast(list[UserRecord], users)
    valid_email = cast(str, email)

    updated_users = deactivate_user_by_email(valid_users, valid_email)

    return UserListResult(
        success=True,
        message="User deactivated.",
        users=updated_users,
    )
