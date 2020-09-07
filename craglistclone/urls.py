from django.urls import path
from . import views, admin

urlpattern=[
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
]
