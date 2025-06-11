from django.shortcuts import render
from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, ProductSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .models import Product
from .permissions import IsSeller, IsBuyer, IsSellerOrReadOnly

User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
# ########login view
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)#authentication ka work krri h

        # if user or pswd match ni kree to yeh refresh krega us user k liye
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user) #yha pr user detail send krskte
            #response m return krdege
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token), #jo detail dalna chate ho isme include
                'user' : user_serializer.data

            })
        else:
            return Response({'detail':'invalid details'}, status=401)
        
        
class LoginView(TokenObtainPairView): #handle and return refresh token + simplejwt
    pass

class ProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller] #only seller can create product

    def perform_create(self, serializer):
        if self.request.user.role != 'seller':
            return Response({"detail": "Only sellers can create products."}) #check krega redundant hora is seller persmision s but good for explicit clarity
        serializer.save(seller=self.request.user)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated] #buyers hi list krskte h all products

class SellerProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsSeller]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user) #seller apna products seen krskta h

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSellerOrReadOnly] #seller crud, buyer read

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.seller:
            return Response({"detail": "You do not have permission to edit this product."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.seller:
            return Response({"detail": "You do not have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)