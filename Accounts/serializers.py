from rest_framework import serializers
from Accounts.models  import User,AddressModel


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'
        
    def create(self, validated_data):
        return AddressModel.objects.created(**validated_data)
        
        

