from django.urls import path
from .views import SubmitData, PerevalDetail

urlpatterns = [
    path('submit_data/', SubmitData.as_view(), name='submit_data'),
    path('submitData/<int:id>/', PerevalDetail.as_view(), name='submit_data_detail'),
]