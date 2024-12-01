from django.shortcuts import render
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from Accounts.models import AddressModel
from Accounts.serializers import AddressSerializers
from utils.StandardResponse import get_Response
from utils.neshan_api import map


class AddressApi(APIView):
    # SERIALIZERS_CLASS = 
    
    def get(self,request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        try:
            if lat and lng:
                    location = map(lat=float(lat),lng=float(lng))
                    return get_Response(success=True,message='آدرس موقعیت مکانی',data=location,status = 200)
        except ValidationError as e:
                return get_Response(
                    success=False,
                    message=e.message,
                    data=None,
                    status= 400
                )
                
    def post(self,request):
        try:
            data = request.data
            ldsrz = AddressSerializers(data=data)            
            if ldsrz.is_valid():
                vd = ldsrz.validated_data
                user_address = AddressModel.objects.create(
                formatted_address = vd.get('formatted_address'),
                state = vd.get('state'),
                county = vd.get('county'),
                neighbourhood = vd.get('neighbourhood')
                )
                # user_address = AddressSerializers.create(validated_data=vd)
                return get_Response(
                    success=True,
                    message='آدرس با موفقیت ثبت شد',
                    data = AddressSerializers(user_address).data,
                    status=201
                )
                
            return get_Response(
                success=False,
                message=ldsrz.errors,
                status=400
            )
                
        except ValidationError as e:
            return get_Response(success=False,message=e.message,status=400)
            
        
        
            
            
                