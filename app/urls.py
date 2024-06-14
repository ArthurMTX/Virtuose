from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import api

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

    # API
    path('pools/', api.get_pools),
    path('domains/', api.get_all_domain),
    path('domains/<str:dom_name>/', api.domain_info_by_name),
    path('domains/UUID/<str:dom_uuid>/', api.dom_info_by_uuid),
    path('domains/actions/<str:dom_uuid>/<str:action>', api.dom_actions),
    path('volumes/', api.volumes_info_all),
    path('volumes/<str:pool_name>/', api.volumes_info)
]
