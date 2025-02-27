from django.urls import path
from .views import upload_csv, get_filtered_sales

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('sales/', get_filtered_sales, name='get_filtered_sales'),
]