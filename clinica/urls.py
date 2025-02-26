from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar', views.registrar, name='registrar'),
     path('editar/<int:registro_id>/', views.editar_registro, name='editar_registro'),
     path('apagar/<int:registro_id>/', views.apagar_registro, name='apagar_registro'),
]