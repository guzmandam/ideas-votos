from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'votos'

urlpatterns = [
    path('', views.index, name='index'), # Página de inicio
    path('login/', auth_views.LoginView.as_view(template_name='votos/login.html'), name='login'), # Página de login
    path('logout/', auth_views.LoginView.as_view(template_name='votos/login.html'), name='logout'), # Página de logout
    path('registro/', views.signup ,name='signup'), # Página de registro
    path('registro/staff/', views.signup_staff, name='signup_staff'), # Página de registro para usuarios staff
    #path('usuario/', views.user, name='usuario'), # Página de usuario (resumen)
    path('listar/', views.list_polls, name='list'), # Página para listar todas las votaciones disponibles
    path('agregar/', views.add_poll, name='add'), # Agregar una nueva votación **admin**
    path('editar/<str:poll_id>/', views.edit_poll, name='edit'), # Editar una votación existente **admin**
    path('borrar/<str:poll_id>/', views.delete_poll, name='delete'), # Borrar una votación existente **admin**
    path('terminar/<str:poll_id>/', views.end_poll, name='end'), # Terminar una votación **admin**
    path('agregar/eleccion/', views.add_choice, name='add_choice'), # Agregar una elección a una votación **admin**
    path('editar/eleccion/<str:choice_id>/', views.edit_choice, name='edit_choice'), # Editar una elección de una votación **admin**
    path('borrar/eleccion/<str:choice_id>/', views.delete_choice, name='delete_choice'), # Editar una elección de una votación **admin**
    path('detalles/<str:poll_id>/', views.detail_poll, name='detail'), # Detalles de una votación 
    path('resultado/<str:poll_id>/', views.result_poll, name='result'),
    path('votar/<str:poll_id>/', views.vote_poll, name='vote'), # Votar en una votación 
]
