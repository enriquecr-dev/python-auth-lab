from auth_lab.foundations.user_data import UserRecord
from auth_lab.foundations.user_service import (
    safe_deactivate_user_by_email,
    safe_find_user_by_email,
)


def main() -> None:
    users: list[UserRecord] = [
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

    lookup_result = safe_find_user_by_email(users, "enrique@example.com")

    print("Lookup result:")
    print(f"Success: {lookup_result.success}")
    print(f"Message: {lookup_result.message}")
    print(f"User: {lookup_result.user}")
    print(f"Errors: {lookup_result.errors}")

    deactivation_result = safe_deactivate_user_by_email(
        users,
        "enrique@example.com",
    )

    print()
    print("Deactivation result:")
    print(f"Success: {deactivation_result.success}")
    print(f"Message: {deactivation_result.message}")
    print(f"Users: {deactivation_result.users}")
    print(f"Errors: {deactivation_result.errors}")

    invalid_result = safe_find_user_by_email(
        users=[
            {
                "id": 1,
                "name": "Bad User",
                "email": True,
                "is_active": True,
                "roles": ["admin"],
            }
        ],
        email="bad@example.com",
    )

    print()
    print("Invalid data result:")
    print(f"Success: {invalid_result.success}")
    print(f"Message: {invalid_result.message}")
    print(f"Errors: {invalid_result.errors}")


if __name__ == "__main__":
    main()
