from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import services

urlpatterns = [
    path("", views.index, name="index"),
    path('action-vms/', views.vm_list, name='action-vms'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register, name='register'),
    path('view/<uuid:vm_uuid>/', views.vm_view, name='vm_view'),
    path('profile/informations', views.informations, name='profile/informations'),
    path('profile/securite', views.securite, name='profile/securite'),
    path('profile/vmlist', views.vm_list, name='profile/vmlist'),
    path('profile/newvm', views.new_vm, name='profile/newvm'),
    path('profile/host', views.host_infos, name='profile/host'),
    path('host_informations/', services.get_host_informations, name='host_informations'),
    path('host_memory/', services.get_host_memory, name='host_memory'),
    path('domains_list/', services.get_all_domains, name='domains_list'),
    path('domain_by_name/<str:name>/', services.get_domain_by_name, name='domain_by_name'),
    path('release_port/', views.release_port, name='release_port'),
]
