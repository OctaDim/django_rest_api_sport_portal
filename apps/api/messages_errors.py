STATUS_NAME_LEN_ERROR_MESSAGE = "The Status name length should be between 3-30"
CATEGORY_NAME_LEN_ERROR_MESSAGE = "The Category name length should be between 4-25"

PASSWORDS_NOT_MATCH_ERROR = "Passwords do not match. Please, try again"
PASSWORD_REQUIRED_MSG = "Empty password. Password is required"
PASSWORD2_REQUIRED_MSG = "Empty repeated password. Repeated password is required"


EMAIL_OR_USERNAME_REQUIRED_MESSAGE = "Empty login name. Email or Username is required"
EMAIL_OR_USERNAME_OR_NICKNAME_REQUIRED_MESSAGE = "Empty login name. Email, Username or Nickname is required"

USERNAME_REQUIRED_MESSAGE = "Empty username. Username is required"
USERNAME_ALREADY_EXISTS = "Such username already exists. Try another username"

NICKNAME_REQUIRED_MESSAGE = "Empty nickname. Nickname is required"
NICKNAME_ALREADY_EXISTS = "Such nickname already exists. Try another nickname"

EMAIL_REQUIRED_MESSAGE = "Empty email. Email is required"
NON_VALID_EMAIL_MESSAGE = "Please, enter a valid email"
EMAIL_ALREADY_EXISTS = "Such email already exists. Try another email"

FIRST_NAME_REQUIRED_MESSAGE = "Empty first name. First name is required"

LAST_NAME_REQUIRED_MESSAGE = "Empty last name. Last name is required"

PHONE_REQUIRED_MESSAGE = "Empty phone number. Phone number is required"

NOT_IS_STAFF_ERROR = "Admin must be staff"
NOT_IS_SUPERUSER_ERROR = "Admin must be a superuser"

NOT_SUPERUSER_FORBIDDEN = "Forbidden. Only superusers can create other superusers accounts"
NOT_STAFF_USER_FORBIDDEN = "Forbidden. Only staff users can create other superusers accounts"


def USER_NOT_FOUND_MESSAGE(username_email_or_nickname: str) -> str:
    return f"User ({username_email_or_nickname}) was not found"


def INVALID_EMAIL_ERROR(email_validation_error: str) -> str:
    return f"{email_validation_error}.\n Please, enter a valid email"
