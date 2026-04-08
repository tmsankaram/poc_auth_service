from rest_framework.serializers import ModelSerializer, Serializer
from ..models import CustomUser


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "company_name",
            "department_code",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
