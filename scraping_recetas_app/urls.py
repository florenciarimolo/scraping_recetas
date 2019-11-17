from django.urls import path, include
from rest_framework import routers

from scraping_recetas_app import views

app_name = 'scraping_recetas_app'
router = routers.DefaultRouter()

router.register('recetas', views.RecetaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categorias/recetas/', views.CategoriaListView.as_view(), name='categorias-recetas')
]
