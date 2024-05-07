from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, Avg
from django.db import models
from django.utils import timezone
    

    

class Vendor(models.Model):
    name = models.CharField(max_length=250)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_unique_code = models.CharField(max_length=50, unique = True, primary_key = True)
    on_time_delivery_date = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfilment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name 

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50,unique =True,primary_key=True)
    Vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    devlivery_data = models.DateTimeField(null=True, blank = True)
    items = models.JSONField()
    
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.po_number 
 
class HistoricalPerformance(models.Model):
    Vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_average = models.FloatField()
    fulfilment_rate = models.FloatField()
    
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.delivered_data is None:
        instance.delivered_data = timezone.now()
        instance.save()
        
    #update on-time delivery rate
    completed_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status ='completed')
    
    #on_time_delivery_rate = completed_orders.filter(delivery_dat__lte=instance.delivery_date).count()/completed_orders.count()
    on_time_deliveries = completed_orders.filter(delivery_date__gte=F('delivered_data'))
    on_time_delivery_rate = on_time_deliveries.count()/completed_orders.count()
    instance.vendor.on_time_delivery_rate = on_time_delivery_date if on_time_delivery_rate else 0
    
    #update quality rating average
    completed_orders_with_rating = completed_orders.exclude(quality_rating__isnull=True)
    quality_rating_avg = completed_orders_with_rating.aggregate(Avg('quality_rating'))['quality_rating_avg']
    instance.vendor.quality_rating_avg = quality-rating_avg if quality_rating_avg else 0
    instance.vendor.save()
    
@receiver(post_save, sender=PurchaseOrder)
def update_response_time(sender, instance, **kwargs):
    #if instance.acknowledgement_date:
    #update average response time
        response_times = PurchaseOrder.objects.filter(vendor=instance.vendor, acknowledgement_date__isnull=False).values_list('acknowledgemt_date','issue_date')
        average_response_time = sum((ack_date - issue_date).total_seconds() for ack_date, issue_date in response_times)
        if average_response_time < 0:
            average_response_time = 0
        if response_times:
            average_response_time = average_response_time / len(response_times)
        else:
            average_response_time = 0
        instance.vendor.average_response_time = average_response_time
        instance.vendor.save()
        
@receiver(post_save, sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance, **kwargs):
    fulfilled_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status="completed")
    fulfilment_rate = fulfilled_orders.count() / PurchaseOrder.objects.filter(vendor=instance.vendor).count()
    instance.vendor.fulfilment_rate = fulfilment_rate
    instance.vendor.save()    
