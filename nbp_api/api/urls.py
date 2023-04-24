from django.urls import path
from . import views


urlpatterns = [
    path('average/<str:code>/<str:date>/', views.rate_per_date),
    path('minimax/<str:code>/<int:number>/', views.minimax_per_period),
    path('diff/<str:code>/<int:number>/', views.biggest_diff),
    path('codes/', views.available_codes),
]
