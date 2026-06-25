from django.contrib import admin
from django.urls import path, include
from catalog.views import (
    HomeView, 
    MachineDetailView, 
    MaintenanceDetailView, 
    ReclamationDetailView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('impersonate/', include('impersonate.urls')),
    path('', HomeView.as_view(), name='home'),
    path('machine/<int:pk>/', MachineDetailView.as_view(), name='machine_detail'),
    path('maintenance/<int:pk>/', MaintenanceDetailView.as_view(), name='maintenance_detail'),
    path('reclamation/<int:pk>/', ReclamationDetailView.as_view(), name='reclamation_detail'),

]
