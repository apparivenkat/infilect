import requests
from django.shortcuts import redirect
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.authentication import  BasicAuthentication
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer, WeatherSerializer
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serialize = self.serializer_class(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return Response({"message": "Logout Successfully"}, status=status.HTTP_200_OK)

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            serialize = self.serializer_class(user)
            # return Response(serialize.data, status=status.HTTP_200_OK)
            return redirect('weather')
        else:
            return Response({"message":"Invalid credential"}, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(login_required(login_url='login'), name='dispatch')
class Weather(ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]  
    serializer_class = WeatherSerializer
    def get(self,request):
        appid = '1e7d616a2561117ee623ff69661dcc1f'
        URL = 'http://api.openweathermap.org/data/2.5/group?id=524901,1269843,1273292,1273309,1273374,1273574,1273637,1273642,1273665,1273673,1273687,1273690,1273704,1273708,1273712,1273724,1273726,1273745,1273780,1273745&units=metric'
        PARAMS = {'appid':appid, "units":'metric'}
        r= requests.get(url=URL, params=PARAMS)
        res = r.json()
        name=res['list']
        country,temp,desc,state = [],[],[],[]
        for i in range(len(name)):
            a=name[i]['sys']['country']
            b=name[i]['main']['temp']
            c=name[i]['weather'][0]['description']
            d=name[i]['name']
            country.append(a)
            temp.append(b)
            desc.append(c)
            state.append(d)
        weather = {}
        weather_list = []
        for i in range(len(country)):
            weather['country'] = country[i]
            weather['temp'] = temp[i]
            weather['desc'] = desc[i]
            weather['state'] = state[i]
            weather_list.append(weather)
            weather = {}    
        return Response({'weather data':weather_list}, status=status.HTTP_200_OK)