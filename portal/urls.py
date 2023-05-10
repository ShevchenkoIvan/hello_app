from django.contrib import admin
from django.urls import path
from . import views
from .views import api_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='home'),
    path('page1', views.page1_view, name='page1'),
    path('stress', views.stress_view, name='stress'),
    path('headers', views.headers_view, name='headers_view'),
    path('status', api_status),

]
