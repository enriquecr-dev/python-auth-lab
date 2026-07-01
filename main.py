from auth_lab.foundations.user_data import (
    UserRecord,
    count_users_by_role,
    find_user_by_email,
    get_active_users,
    get_unique_roles,
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
            "name": "Cristina",
            "email": "cristi@example.com",
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

    active_users = get_active_users(users)
    user = find_user_by_email(users, "enrique@example.com")
    unique_roles = get_unique_roles(users)
    role_counts = count_users_by_role(users)

    print(f"Active users: {len(active_users)}")
    print(f"Found user: {user}")
    print(f"Unique roles: {unique_roles}")
    print(f"Role counts: {role_counts}")


if __name__ == "__main__":
    main()
