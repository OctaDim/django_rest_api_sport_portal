from apps.api.user.serializer_user_reg import UserRegistrySerializer

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################





# ######################################################################
# ########################## TRIAL CODE ################################
# ######################################################################

class _Test_UserRegistrySerializer(UserRegistrySerializer):  # Inherited from the ordinal user serializer
    # def validate(self, attrs):  # Option 1: To assign value into the fields set default in the Model
    #     super().validate(attrs)  # Completion of all checks defined in custom UserRegistrySerializer (can be abstract)
    #     attrs["is_staff"] = "False"  # Redefined default value (if determined in the model fields parameters)
    #     attrs["is_superuser"] = "False"  # Redefined default value (if determined in the model fields parameters)
    #     attrs["is_verified"] = "False"  # Redefined default value (if determined in the model fields parameters)
    #     return attrs

    def create(self, validated_data):  # Option 2: To assign value into the fields set default in the Model
        validated_data.pop("password2")  # Refactored to avoid tedious getting values from validated_data via get()
        user = User.objects._test_create_any_type_user(
            # is_staff=False,  # Can be defined directly here or in validate method
            # is_superuser=False,  # Can be defined directly here or in validate method
            # is_verified=False,  # Can be defined directly here or in validate method
            **validated_data)
        return user


class _Test_SuperUserRegistrySerializer(UserRegistrySerializer):  # Inherited from the ordinal user serializer
    def validate(self, attrs):  # Option 1: To assign value into the fields set default in the Model
        super().validate(attrs)  # Completion of all checks defined in custom UserRegistrySerializer (can be abstract)
        attrs["is_staff"] = "True"  # Redefined default value (if determined in the model fields parameters)
        attrs["is_superuser"] = "True"  # Redefined default value (if determined in the model fields parameters)
        # attrs["is_verified"] = "False"  # Redefined default value (if determined in the model fields parameters)
        return attrs

    def create(self, validated_data):  # Option 2: To assign value into the fields set default in the Model
        validated_data.pop("password2")  # Refactored to avoid tedious getting values from validated_data via get()
        user = User.objects._test_create_any_type_user(
            # is_staff=True,  # Can be defined directly here or in validate method
            # is_superuser=True,  # Can be defined directly here or in validate method
            # is_verified=False,  # Can be defined directly here or in validate method
            **validated_data)
        return user

class _Test_StaffUserRegistrySerializer(UserRegistrySerializer):  # Inherited from the ordinal user serializer
    def validate(self, attrs):  # Option 1: To assign value into the fields set default in the Model
        super().validate(attrs)  # Completion of all checks defined in custom UserRegistrySerializer (can be abstract)
        attrs["is_staff"] = "True"  # Redefined default value (if determined in the model fields parameters)
        attrs["is_superuser"] = "False"  # Redefined default value (if determined in the model fields parameters)
        # attrs["is_verified"] = "False"  # Redefined default value (if determined in the model fields parameters)
        return attrs

    def create(self, validated_data):  # Option 2: To assign value into the fields set default in the Model
        validated_data.pop("password2")  # Refactored to avoid tedious getting values from validated_data via get()
        user = User.objects._test_create_any_type_user(
                # is_staff=True,  # Can be defined directly here or in validate method
                # is_superuser=False,  # Can be defined directly here or in validate method
                # is_verified=False,  # Can be defined directly here or in validate method
                **validated_data)
        return user
# ######################################################################
# ######################################################################
# ######################################################################
