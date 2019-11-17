from django.urls import path, include
from rest_framework import routers

from scraping_recetas_app import views

app_name = 'scraping_recetas_app'
router = routers.DefaultRouter()

router.register('recetas', views.RecetaListView)

urlpatterns = [
    path('', include(router.urls)),
]
