from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import os


from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import views as drf_views
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers

from .models import LogoEntries
from .serializers import LogoModelSerializer


class LogoViewSet(viewsets.ModelViewSet):
    
    queryset = LogoEntries.objects.all()
    serializer_class = LogoModelSerializer