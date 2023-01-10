

from django.urls import path
from .views import *

urlpatterns = [
    path('', LotofacilView.as_view(), name='index'),
    path('tests', TestView.as_view(), name='tests'),
    path('add', NewGameFormView.as_view(), name='add'),
]
