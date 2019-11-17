from django.urls import path, include
from rest_framework import routers

from scraping_recetas_app import views

app_name = 'scraping_recetas_app'
router = routers.SimpleRouter()

router.register('recetas', views.RecetaViewSet, base_name='receta')

urlpatterns = [
    path('', views.APIRoot.as_view(), name='root'),
    path('', include(router.urls)),
    path('categorias/recetas/', views.CategoriaListView.as_view(), name='categorias-recetas')
]
