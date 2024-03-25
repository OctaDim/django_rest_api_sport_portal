from apps.api.utils.utils import number_or_str_to_int
from apps.api.utils.utils import validate_level_value
from apps.api.self_satisfaction_level.settings import (
    SATISFACTION_LEVEL_VALUE_MIN_LIMIT,
    SATISFACTION_LEVEL_VALUE_MAX_LIMIT)


def validate_satisfaction_level_value(value):
    level_min_limit = number_or_str_to_int(SATISFACTION_LEVEL_VALUE_MIN_LIMIT)
    level_max_limit = number_or_str_to_int(SATISFACTION_LEVEL_VALUE_MAX_LIMIT)
    validate_level_value(value, level_min_limit, level_max_limit)
