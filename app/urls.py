from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views
from . import routes

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="API description",
      terms_of_service="https://www.yourcompany.com/terms/",
      contact=openapi.Contact(email="contact@yourcompany.com"),
      license=openapi.License(name="Your License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url='http://virtuose/',  # Assurez-vous que cette URL est correcte et accessible.
   patterns=[
       path('api/pools/', routes.get_pools),
       path('api/domains/', routes.get_all_domain),
       path('api/domains/<str:dom_name>/', routes.domain_info_by_name),
       path('api/domains/UUID/<str:dom_uuid>/', routes.dom_info_by_uuid),
       path('api/domains/actions/<str:dom_uuid>/<str:action>', routes.dom_actions),
       path('api/volumes/', routes.volumes_info_all),
       path('api/volumes/<str:pool_name>/', routes.volumes_info),
       path('api/hosts/', routes.get_host_info)
   ],
   config={
       'validatorUrl': None  # Désactiver la validation en ligne
   }
)

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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/pools/', routes.get_pools),
    path('api/domains/', routes.get_all_domain),
    path('api/domains/<str:dom_name>/', routes.domain_info_by_name),
    path('api/domains/UUID/<str:dom_uuid>/', routes.dom_info_by_uuid),
    path('api/domains/actions/<str:dom_uuid>/<str:action>', routes.dom_actions),
    path('api/volumes/', routes.volumes_info_all),
    path('api/volumes/<str:pool_name>/', routes.volumes_info),
    path('api/hosts/', routes.get_host_info)
]
