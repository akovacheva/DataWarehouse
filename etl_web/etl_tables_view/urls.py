from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_func),
    path('table/<str:table_name>/', views.users, name='table'),
    path('datable/<str:table_name>/', views.datatable, name='datatable'),

]
