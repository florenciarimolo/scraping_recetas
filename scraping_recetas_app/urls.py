from django.urls import path, include
from rest_framework import routers

from scraping_recetas_app import views

app_name = 'scraping_recetas_app'
router = routers.SimpleRouter()

urlpatterns = [
    path('', views.APIRoot.as_view(), name='root'),
    path('', include(router.urls)),
    path('categorias', views.CategoriaListView.as_view(), name='categorias-recetas'),
    path('categorias/<int:id_categoria>/subcategorias', views.SubcategoriaListView.as_view(), name='subcategoria-list'),
    path('categorias/<int:id_categoria>/subcategorias/<int:pk>', views.SubcategoriaView.as_view(), name='subcategoria-detail'),
    path('categorias/<int:id_categoria>/subcategorias/<int:id_subcategoria>/recetas', views.RecetaListView.as_view(), name='receta-list'),
    path('categorias/<int:id_categoria>/subcategorias/<int:id_subcategoria>/recetas/<int:pk>', views.RecetaView.as_view(), name='receta-detail'),
]
