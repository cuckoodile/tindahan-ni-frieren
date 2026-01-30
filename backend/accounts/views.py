from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from utils.permissions import OwnerOrStaff
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView

from .models import *
from .serializers import *

# Create your views here.

# User Views
class UserListAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            return [IsAuthenticated(), OwnerOrStaff()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
        else:
            return [AllowAny()]

class OwnerListAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, OwnerOrStaff]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return CustomUser.objects.none()

        # Return a queryset containing only the requesting user
        return CustomUser.objects.filter(id=self.request.user.id)
    
class CustomerCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class StaffCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True)

class AdminCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_superuser=True)