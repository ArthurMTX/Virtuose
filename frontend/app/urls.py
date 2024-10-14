"""URLs for the frontend app."""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import services
from .views import (
    IndexView,
    RegisterView,
    LoginView,
    InformationsView,
    SecurityView,
    NewVMView,
    VMListView,
    VMView,
    ReleasePortView,
    HostInfosView,
    PoolsInfosView,
)

urlpatterns = [
    # === HOME & AUTH ===
    path("", IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # === VM ACTIONS ===
    path('action-vms/', VMListView.as_view(), name='action-vms'),
    path('view/<str:vm_name>/', VMView.as_view(), name='vm_view'),

    # === USER PROFILE ===
    path('profile/informations', InformationsView.as_view(), name='profile/informations'),
    path('profile/securite', SecurityView.as_view(), name='profile/securite'),
    path('profile/vmlist', VMListView.as_view(), name='profile/vmlist'),
    path('profile/newvm', NewVMView.as_view(), name='profile/newvm'),

    # === SERVICES: HOST & VM INFORMATION ===
    path('profile/host', HostInfosView.as_view(), name='profile/host'),
    path('host_informations/', services.get_host_informations, name='host_informations'),
    path('host_memory/', services.get_host_memory, name='host_memory'),
    path('domains_list/', services.get_all_domains, name='domains_list'),
    path('domain_informations/<str:dom_name>/', services.get_domain_informations, name='domain_informations'),

    # === SERVICES: POOLS ===
    path('profile/pools', PoolsInfosView.as_view(), name='profile/pools'),

    # === SERVICES: VM ACTIONS ===
    path('release_port/', ReleasePortView.as_view(), name='release_port'),
    path('domains/start/<str:dom_name>/', services.start_domain, name='start_domain'),
    path('domains/stop/<str:dom_name>/', services.stop_domain, name='stop_domain'),
    path('domains/force_stop/<str:dom_name>/', services.force_stop_domain, name='force_stop_domain'),
    path('domains/delete/<str:dom_name>/', services.delete_domain, name='delete_domain'),
    path('domains/restart/<str:dom_name>/', services.restart_domain, name='restart_domain'),
]
