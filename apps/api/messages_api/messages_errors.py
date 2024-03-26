STATUS_NAME_LEN_ERROR_MESSAGE = "The Status name length should be between 3-30"
CATEGORY_NAME_LEN_ERROR_MESSAGE = "The Category name length should be between 4-25"

PASSWORD_REQUIRED_MSG = "Empty password. Password is required"
PASSWORD2_REQUIRED_MSG = "Empty repeated password. Repeated password is required"
PASSWORDS_NOT_MATCH_ERROR = "The two password fields did not match. Please, try again"

DEPARTMENT_NAME_REQUIRED = "Department name is required. Fill department field"
COMPANY_NAME_REQUIRED = "Company is required. Select company"

TRAINING_GROUP_CODE_REQUIRED = "Training group is required. Fill training group code field"

START_DATE_REQUIRED = "Start date is required. Fill start date field"
FINISH_DATE_REQUIRED = "Finish date is required. Fill finish date field"

CLIENT_STATUS_REQUIRED = "Client status is required. Fill client status field"
COACH_SPECIALITY_REQUIRED = "Coach speciality is required. Fill coach speciality field"
COMPANY_REQUIRED = "Company name is required. Fill company field"
COUNTRY_REQUIRED = "Country name is required. Fill country field"
GENDER_REQUIRED = "Gender name is required. Fill country field"
PAYMENT_DOCUMENT_REQUIRED = "Payment document name is required. Fill payment document field"
PAYMENT_TYPE_REQUIRED = "Payment type name is required. Fill payment type field"
TRAINING_YEAR_REQUIRED = "Training year (period) name is required. Fill training year field"



EMOTIONAL_LEVEL_NAME_REQUIRED = "Emotional level name is required. Fill this field"
SATISFACTION_LEVEL_NAME_REQUIRED = "Self satisfaction level name is required. Fill this field"

SATISFACTION_LEVEL_VALUE_REQUIRED = "Self satisfaction level value is required. Fill this field"
EMOTIONAL_LEVEL_VALUE_REQUIRED = "Emotional level value is required. Fill this field"

GROUP_CLIENT_REQUIRED = "Group-Client is required. Select Group-Client"
SELF_SATISFACTION_LEVEL_REQUIRED = "Self satisfaction level is required. Select this level"
EMOTIONAL_LEVEL_REQUIRED = "Emotional level is required. Select emotional level"
CHECK_POINT_DATE_REQUIRED = "Checkpoint date is required. Fill checkpoint date field"

GROUP_CLIENT_DATE_EXISTS = "Group-Client-Progress with this date already exists. Try again"

NEGATIVE_NUMBER_OR_STRING = "Invalid format, negative number or string. Must be a positive number"

DEPARTMENT_REQUIRED = "Department is required. Select department"
TRAINING_YEAR_REQUIRED = "Training year is required. Select training year"

ADMINISTRATOR_REQUIRED = "Administrator is required. Select creator"
CREATOR_REQUIRED = "Creator is required. Select creator"

USER_CREATOR_REQUIRED = "User creator is required. Select user creator"

USER_REQUIRED = "User is required. Select user"

DEPARTMENT_NAME_ALREADY_EXISTS = "Department with this name already exists. Try another name"
TRAINING_GROUP_CODE_ALREADY_EXISTS = "Training group with this code already exists. Try another code"

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

EMOTIONAL_LEVEL_VALUE_EXISTS = "Emotional level with this level value already exists. Try again"
EMOTIONAL_LEVEL_NAME_EXISTS = "Emotional level with this name already exists. Try again"
CLIENT_STATUS_EXISTS = "Client status with this name already exists. Try again"
COACH_SPECIALITY_EXISTS = "Coach speciality with this name already exists. Try again"
COMPANY_EXISTS = "Company with this name already exists. Try again"
COUNTRY_EXISTS = "Country with this name already exists. Try again"
GENDER_EXISTS = "Gender with this name already exists. Try again"
PAYMENT_DOCUMENT_EXISTS = "Payment document with this name already exists. Try again"
PAYMENT_TYPE_EXISTS = "Payment type with this name already exists. Try again"
TRAINING_YEAR_EXISTS = "Training year (period) with this name already exists. Try again"


SATISFACTION_LEVEL_VALUE_EXISTS = "Self satisfaction level with this value already exists. Try again"
SATISFACTION_LEVEL_NAME_EXISTS = "Self satisfaction with this name already exists. Try again"

FIRST_NAME_REQUIRED_MESSAGE = "Empty first name. First name is required"

LAST_NAME_REQUIRED_MESSAGE = "Empty last name. Last name is required"

PHONE_REQUIRED_MESSAGE = "Empty phone number. Phone number is required"

SUPERUSER_NOT_IS_STAFF_ERROR = "Superuser must be staff"
SUPERUSER_NOT_IS_SUPERUSER_ERROR = "Superuser must be superuser"

STAFF_NOT_IS_STAFF_ERROR = "Staff must be staff"

TRAINER_NOT_IS_TRAINER_ERROR = "Trainer must be trainer"

NOT_SUPERUSER_FORBIDDEN = "Forbidden. Only superuser can create other superusers accounts"
NOT_STAFF_USER_FORBIDDEN = "Forbidden. Only staff user can create other staff users accounts"

NOT_SUPERUSER_HARD_DELETE_FORBIDDEN = "Forbidden. Only superuser can make hard deleting operation"

HARD_DELETE_FORBIDDEN_CLIENT_REFS_EXIST = "Hard delete is forbidden. Remove clients from this training group first"

DELETE_YOURSELF_FORBIDDEN = "Forbidden. As Superuser, you cannot delete yourself"
INACTIVE_YOURSELF_FORBIDDEN = "Forbidden. You cannot make yourself inactive"

NOT_AUTHENTICATED_USER_FORBIDDEN = "Forbidden. You are not authenticated"


def USER_NOT_FOUND_MESSAGE(username_email_or_nickname: str) -> str:
    return f"User [ {username_email_or_nickname} ] was not found"

def INVALID_EMAIL_ERROR(email_validation_error: str) -> str:
    return (f"Email [ {email_validation_error} ] is not valid. "
            f"Please, enter a valid email")

def MAXIMUM_FILE_SIZE(max_file_size_limit: float) -> str:
    return (f"File size error. "
            f"Maximum file size is {max_file_size_limit} Megabyte")

def NOT_POSITIVE_FLOAT_OR_INT(field_name: str, field_value: any) -> str:
    return (f"Field '{field_name}' value ({field_value}) "
            f"is not valid positive number. Try again")

def NOT_INTEGER_NUMBER(field_name: str, field_value: any) -> str:
    return (f"Field '{field_name}' value ({field_value}) "
            f"is not valid integer number. Try again")

def LEVEL_VALUE_MIN_LIMIT(value: any, min_limit: any) -> str:
    return (f"Level value ({value}) is less "
            f"minimum limit ({min_limit}). Try again")

def LEVEL_VALUE_MAX_LIMIT(value: any, max_limit: any) -> str:
    return (f"Level value ({value}) is bigger "
            f"maximum limit ({max_limit}). Try again")
