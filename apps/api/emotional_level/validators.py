from apps.api.utils.utils import number_or_str_to_int
from apps.api.utils.utils import validate_level_value
from apps.api.emotional_level.settings import (EMOTIONAL_LEVEL_VALUE_MIN_LIMIT,
                                               EMOTIONAL_LEVEL_VALUE_MAX_LIMIT)


def validate_emotional_level_value(value):
    level_min_limit = number_or_str_to_int(EMOTIONAL_LEVEL_VALUE_MIN_LIMIT)
    level_max_limit = number_or_str_to_int(EMOTIONAL_LEVEL_VALUE_MAX_LIMIT)
    validate_level_value(value, level_min_limit, level_max_limit)
