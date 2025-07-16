from django.urls import path
from .views import SubmitData, PerevalRetrieveUpdateView

urlpatterns = [
    path('submit_data/', SubmitData.as_view(), name='submit_data'),
    path('submitData/<int:id>/', PerevalRetrieveUpdateView.as_view(), name='submit_data_detail'),
]