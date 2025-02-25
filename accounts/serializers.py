from rest_framework import serializers
from models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            
        )


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    type_account = serializers.ChoiceField(choices=['owner', 'employee'], default='owner')
    company_id = serializers.IntegerField(required=False)