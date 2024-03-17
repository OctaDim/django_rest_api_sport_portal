STATUS_NAME_LEN_ERROR_MESSAGE = "The Status name length should be between 3-30"
CATEGORY_NAME_LEN_ERROR_MESSAGE = "The Category name length should be between 4-25"

PASSWORD_REQUIRED_MSG = "Empty password. Password is required"
PASSWORD2_REQUIRED_MSG = "Empty repeated password. Repeated password is required"
PASSWORDS_NOT_MATCH_ERROR = "The two password fields did not match. Please, try again"

USER_CREATOR_REQUIRED = "User creator is required. Select user creator"

USER_REQUIRED = "User is required. Select user"

CLIENT_CREATOR_REQUIRED = "Client creator is required. Select client creator"
CLIENT_WITH_USER_ALREADY_EXISTS = "Client with this user already exists. Select another user"

ADMINISTRATOR_CREATOR_REQUIRED = "Administrator creator is required. Select client creator"
ADMINISTRATOR_WITH_USER_ALREADY_EXISTS = "Administrator with this user already exists. Select another user"

COACH_CREATOR_REQUIRED = "Coach creator is required. Select client creator"
COACH_WITH_USER_ALREADY_EXISTS = "Coach with this user already exists. Select another user"

EMAIL_OR_USERNAME_REQUIRED_MSG = "Empty login name. Email or Username is required"
EMAIL_OR_USERNAME_OR_NICKNAME_REQUIRED_MSG = "Empty login name. Email, Username or Nickname is required"

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

SUPERUSER_NOT_IS_STAFF_ERROR = "Superuser must be staff"
SUPERUSER_NOT_IS_SUPERUSER_ERROR = "Superuser must be superuser"

STAFF_NOT_IS_STAFF_ERROR = "Staff must be staff"

TRAINER_NOT_IS_TRAINER_ERROR = "Trainer must be trainer"

NOT_SUPERUSER_FORBIDDEN = "Forbidden. Only superuser can create other superusers accounts"
NOT_STAFF_USER_FORBIDDEN = "Forbidden. Only staff user can create other staff users accounts"

DELETE_YOURSELF_FORBIDDEN = "Forbidden. As Superuser, you cannot delete yourself"
INACTIVE_YOURSELF_FORBIDDEN = "Forbidden. You cannot make yourself inactive"

NOT_AUTHENTICATED_USER_FORBIDDEN = "Forbidden. You are not authenticated"

def USER_NOT_FOUND_MESSAGE(username_email_or_nickname: str) -> str:
    return f"User [ {username_email_or_nickname} ] was not found"


def INVALID_EMAIL_ERROR(email_validation_error: str) -> str:
    return f"Email [{email_validation_error}] validation error. Please, enter a valid email"

def MAXIMUM_FILE_SIZE(max_file_size_limit: float) -> str:
    return f"File size error. Maximum file size is {max_file_size_limit} Megabyte"
