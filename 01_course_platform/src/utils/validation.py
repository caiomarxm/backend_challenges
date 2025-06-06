import re


def is_email_valid(email: str) -> bool:
    EMAIL_REGEX = re.compile(
        r"^(?!\.)[a-zA-Z0-9_.+-]+(?<!\.)@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    )

    return bool(EMAIL_REGEX.match(email))
