from rest_framework import serializers
from Accounts.models  import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

