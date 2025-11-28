from django.contrib import admin
from django.urls import path, include
urlpatterns = [
  path('', include(('frontend.urls','frontend'),namespace='frontend')),
  path('', include('catalog.urls', namespace='catalog')),
  path('', include('sales.urls', namespace='sales')),
  path('', include('inventory.urls', namespace='inventory')),
  path('admin/', admin.site.urls),
]
admin.site.site_header="Inventory Management (Single Shop)"
admin.site.site_title="Inventory Admin"
admin.site.index_title="Dashboard"
