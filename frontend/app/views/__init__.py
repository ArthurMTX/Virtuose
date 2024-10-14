from .base_views import IndexView
from .auth_views import (
    RegisterView,
    LoginView,
    ProfileView,
    InformationsView,
    SecurityView,
)
from .vm_views import NewVMView, VMListView, VMView, ReleasePortView
from .host_views import HostInfosView, PoolsInfosView