from django.urls import path
from . import views, admin

urlpattern=[
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('new_search', views.new_search, name='new_search'),
]
