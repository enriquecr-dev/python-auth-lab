from auth_lab.foundations.user_validation import (
    normalize_email,
    validate_registration_data,
)


def main() -> None:
    name = " Enrique"
    email = "Enrique@Example.COM"
    password = "Password123!"

    errors = validate_registration_data(name=name, email=email, password=password)

    if errors:
        print("Registration rejected:")

        for error in errors:
            print(f"- {error}")

        return

    print("Registration accepted.")
    print(f"Normalized email: {normalize_email(email)}")


if __name__ == "__main__":
    main()
