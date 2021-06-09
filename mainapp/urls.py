from django.urls import path
from . import views
urlpatterns = [
    path('pick',views.stockPicker, name="stockpicker"),
    path('track',views.stockTracker, name="stocktracker")

]
