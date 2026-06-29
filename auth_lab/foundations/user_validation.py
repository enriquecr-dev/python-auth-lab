MIN_PASSWORD_LENGTH = 12


def normalize_text(value: str) -> str:
    return value.strip()


def normalize_email(email: str) -> str:
    return email.strip().lower()


def is_valid_email(email: str) -> bool:
    cleaned_email = normalize_email(email)

    if cleaned_email.count("@") != 1:
        return False

    local_part, domain_part = cleaned_email.split("@", maxsplit=1)

    if not local_part:
        return False

    if not domain_part:
        return False

    if "." not in domain_part:
        return False

    if domain_part.startswith(".") or domain_part.endswith("."):
        return False

    return True


def is_strong_password(password: str) -> bool:
    if len(password) < MIN_PASSWORD_LENGTH:
        return False

    has_uppercase = any(character.isupper() for character in password)
    has_lowercase = any(character.islower() for character in password)
    has_digit = any(character.isdigit() for character in password)
    has_especial_character = any(not character.isalnum() for character in password)

    return has_uppercase and has_lowercase and has_digit and has_especial_character


def validate_registration_data(name: str, email: str, password: str) -> list[str]:
    errors: list[str] = []

    cleaned_name = normalize_text(name)

    if not cleaned_name:
        errors.append("Name is required.")

    if cleaned_name and len(cleaned_name) < 2:
        errors.append("Name must have at least 2 characters.")

    if not is_valid_email(email):
        errors.append("Email is not valid.")

    if not is_strong_password(password):
        errors.append(
            "Password must have at least 12 characters, uppercase, lowercase, "
            "number, and special character."
        )

    return errors
