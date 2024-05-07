from django.shortcuts import render
from rest_framework.generics import GenericAPIView 
from rest_framework.mixins import * 
from .models import *
from .serializers import * 
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status

class VendorListCreateView(generics.ListCreateAPIView):
    #authentication_classes = [tokenAuthentictaion]
    #permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = PurchaseOrderSerializer
    
class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'on_time_delivery_rate': serializer.data['on_time_delivery_rate'],
                'quality_rating-avg': serializer.data['quality_rating_avg'],
                'average_response_time': serializer.data['average_response_time'],
                'fulfilment_rate': serializer.data['fulfilment_rate']})
    
class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    