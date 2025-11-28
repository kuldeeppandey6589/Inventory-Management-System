from django.urls import path
from . import views
app_name='frontend'

urlpatterns= [ 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    path('logout/',views.logout,name='logout'),
    path('stock_move/',views.stock_move,name='stock_move'),
    path('logout_view',views.logout_view,name='logout_view'),
]
                                                                            