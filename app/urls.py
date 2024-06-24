from django.urls import path
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView

from . import views
from . import routes

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
    path('release_port/', views.release_port, name='release_port'),

    # API
    path('api/', SpectacularAPIView.as_view(), name='Virtuose API'),
    path('api/pools/', routes.get_pools),
    path('api/domains/', routes.get_all_domain),
    path('api/domains/<str:dom_name>/', routes.domain_info_by_name),
    path('api/domains/UUID/<str:dom_uuid>/', routes.dom_info_by_uuid),
    path('api/domains/actions/<str:dom_uuid>/<str:action>', routes.dom_actions),
    path('api/volumes/', routes.volumes_info_all),
    path('api/volumes/<str:pool_name>/', routes.volumes_info),
    path('api/hosts/', routes.get_host_info)
]
